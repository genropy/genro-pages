## Phase 1

Approved: use the core cookie reader, validate the connection in the worker, register before HTML and let the front emit its cookie. Native ASGI, toolbox IDs, no parallel registry.

Owner clarification: legacy is experience, not the specification of the new product. Preserve ideas that still solve current problems; reject weak or obsolete mechanisms with an explicit reason. Compatibility is valuable but not an unconditional implementation constraint.

Legacy evidence: GnrWebPage._register_new_page creates a connection if absent, creates an ID, registers page metadata, then calls onPageRegistered. ConnectionProxy validates both registration and user. The header embeds page_id in GenroClient construction. We preserve registration-before-document and ownership validation; no Mako, marshal cookie, secondary async registration or arbitrary old callback surface is copied.

Core: 0.43.1 is available from the package index. Incoming cid is not exposed as a scope field; use the core cookie_value helper, never request_slot.connection_id (output-only). The existing local builders 0.23.2 is not yet on the package index and remains a local test dependency.

Implementation: PageWorker hosts one DemoApplication in PageServer. PageServer overrides the existing run_sync seam so synchronous routes use the worker traffic pool and request-slot context. Asset reads also use that pool. Incoming cid is checked against the core's user identity before reuse. No new registration callback API was added without a current consumer. Direct rendering remains available for isolated recipe tests; the CLI uses registered hosting.

Validation: isolated Python 3.12 environment with published genro-asgi 0.43.1, toolbox 0.14.0 and TYTX 0.14.0; existing local builders/bag source paths are required for the JS compatibility baseline. 84 tests passed before two additional integration/edge tests were added. Real front PID 31822 and worker PID 31855 on port 8013: distinct page IDs, one connection, HttpOnly cookie, unknown page 404, both registered channels opened with status 200. Permanent subprocess test reproduces this without diagnostic application endpoints. Freeze/resume was not tested.

Launch: PYTHONPATH=src:../genro-builders/src:../genro-bag/src:../genro-tytx/src temp/registered-startup-venv/bin/python -m genro_pages --modules .. --port 8013 --state-dir /tmp/genro-pages-registered

Configuration corrections during verification: pass the configuration builder instance (not its SourceBag); provide the core-required worker entry_module. Socket binding requires sandbox escalation. Default state uses a short /tmp path to respect Unix socket limits.

Final verification: 86 tests passed in 52.76s with the permanent real-server test included; ruff check src tests and git diff --check clean. Read-only independent review found no actionable phase-1 defects. The three plan contract names and wf:contract lines remain intact, and the committed plan test copy is unchanged. Source transport and iframe lifecycle remain Phase 2/later scope.

### Naming review (Phase 1)

All entries are required; no speculative helper was retained.

| Proposed name | Kind | File | Phase |
| --- | --- | --- | --- |
| PageServer.__init__ | framework constructor; class name free | src/genro_pages/worker.py | 1 |
| PageServer.run_sync | framework override; delegates to the worker pool with argument binding | src/genro_pages/worker.py | 1 |
| PageWorker.__init__ | framework constructor; class name free | src/genro_pages/worker.py | 1 |
| PageConfiguration.__init__ | framework constructor; class name free | src/genro_pages/server_configuration.py | 1 |
| PageConfiguration.main | framework recipe entry | src/genro_pages/server_configuration.py | 1 |
| RegisteredPageChecks.__init__ | framework constructor; test class name free | tests/test_registered_page.py | 1 |
| RegisteredPageChecks.get_document | free | tests/test_registered_page.py | 1 |
| RegisteredPageChecks.get_startup | free | tests/test_registered_page.py | 1 |
| registered_pages | free pytest fixture name | tests/test_registered_page.py | 1 |
| test_html_identity_is_already_registered | plan contract name | tests/test_registered_page.py | 1 |
| test_page_loads_have_distinct_identities | plan contract name | tests/test_registered_page.py | 1 |
| test_unknown_page_does_not_register | plan contract name | tests/test_registered_page.py | 1 |
| test_wrong_user_cannot_reuse_connection | test prefix fixed; suffix free | tests/test_registered_page.py | 1 |
| test_stale_cookie_creates_a_new_connection | test prefix fixed; suffix free | tests/test_registered_page.py | 1 |
| test_real_worker_registers_pages_before_their_channels_open | test prefix fixed; suffix free | tests/test_registered_server.py | 1 |

Naming review: owner accepted all names. Markers removed without behavioral changes. Closing contract comparison and skeleton integrity checks passed. No human verification remains for phase 1.


## Phase 2 — ownership and distribution decision

The owner approved this architectural direction in conversation:
- Keep genro-dom-js as an independent JavaScript construction/rendering library, usable without pages or an ASGI backend.
- Keep Python and the JavaScript specific to page integration in the genro-pages repository. No genro-pages-js repository or blanket rename of genro-dom-js is selected.
- Use src/genro_pages for Python and js/src for shared integration JavaScript; page-specific JS/CSS may remain beside page recipes under the future resource convention.
- Package compatible integration JS/CSS in the genro-pages wheel. End-user installation must not require npm or compilation; release-time preparation is distinct from browser asset delivery.
- The DOM library may be published independently as ESM/npm. A pages release should include a precise tested set of necessary browser dependencies. CDN delivery is optional, not required.

Covering plan edit: added ownership/distribution Must not break headers and clarified Phase 2 Details. Existing acceptance tests are unchanged. The actual source relocation, generic mount API and packaging implementation are not claimed complete; detailed integration scope still needs the phase gate after this architectural clarification.

Preflight evidence: Application currently mounts in its constructor and BuilderBase.loadSource rejects mounted builders. A clean delayed-mount boundary must be designed rather than worked around through bootstrap internals. Core WSX rehydrates JSON/MessagePack hosted responses and emits TYTX JSON text; MessagePack response selection is not a binary WebSocket transport. Hosted source selection must follow the registered page and its owning connection.

### Legacy RPC audit before Phase 2 implementation

Owner explicitly requested reviewing serverCall and preserving the WSK convention before building the new RPC proxy/dataRpc integration.

Verified legacy references (root /Users/gporcari/Sviluppo/Genropy/genropy):
- gnrjs/gnr_d11/js/genro.js:2199, genro.serverCall(method, params, async_cb, mode, httpMethod), defaults to POST and delegates to genro.rpc.remoteCall.
- gnrjs/gnr_d11/js/genro_rpc.js:267: proxy serverCall is empty; it is NOT the actual entry point. remoteCall at 450 dispatches WSK directly to genro.wsk.call; _serverCall/_serverCall_execute are HTTP-specific.
- gnrjs/gnr_d11/js/gnrdomsource.js:391: dataRpc extracts httpMethod; otherwise _POST=False means GET, default POST. _onCalling may veto before transport; _onResult/_onError execute with source-node context. Destination is written before _onResult, and callback arguments include the evaluated original kwargs.
- gnrjs/gnr_d11/js/gnrwebsocket.js:121/205: waitingCalls[result_token] correlates replies. No per-call timeout or close rejection in this path. Missing socket resolves null. Business errors resolve an error object instead of rejecting. Result is a data node; BagNode.setValue unwraps it for destination storage, but callbacks can still observe a node.
- projects/gnrcore/packages/test15/webpages/ws/dbselect_ws.py and testcomunication.py demonstrate dataRpc(..., httpMethod='WSK') alongside normal data binding.

Keep the distinction: method names the remote operation; httpMethod='WSK' selects WebSocket transport. WSK is a Genro convention, not a network HTTP verb. In the new core it maps to the existing WSX synthetic WSK request, without copying the legacy result_token/XML protocol.

Do not accidentally reproduce legacy divergence: HTTP remoteCall can become synchronous when no callback is supplied, whereas WSK always returns a Deferred; WSK bypasses HTTP mode/timeout and response side-effect processing; result node/value shapes and callback-chain returns differ. Prefer a consistent Promise-based core with explicit compatibility adaptation where a real consumer needs it. Reject unavailable/closed/timed-out requests; never interpret an absent socket as a successful null result. Client cancellation does not imply cancellation of server work.

DataRpc concurrency is not implemented by _lastDeferred: it only records a reference, and each completion may overwrite the destination. A latest-result policy for repeat calls on the same source node is a new semantic decision, not a legacy behavior to claim. General page RPC must retain independent correlated calls; automatic replay of side-effecting calls after reconnection is not implied.

The new pages RPC service must be the transport dependency of future dataRpc, not a second implementation hidden in the data provider. This does not claim that dataRpc grammar/runtime support already exists. HTTP versus WSK defaults for new recipes remain an owner decision; Phase 2 startup can select WSK explicitly.

### Confirmed RPC transport configuration

The owner confirmed WSK as the initial RPC default, redefinable through application configuration. An explicit per-call `httpMethod` overrides this default; `method` remains the remote operation. Native registered startup opens its page channel independently of the RPC default. POST/GET must remain explicit alternatives, with no automatic retry of failed WebSocket mutations through HTTP. The owner authorized changes in both pages and DOM for the generic deferred mount and integration.

### Phase 2 implementation and verification

- `genro-dom-js` keeps generic `Application(host, builder)` and now also supports
  `Application(host)` followed by one `mountBuilder(builder)`. Data and service
  identities survive mounting. Failed mounting disposes the partial runtime and
  rethrows; repeated or late mounts are rejected. 131 DOM tests pass.
- Pages owns `js/src/application.js` and `rpc.js`: `PageApplication` extends the
  generic runtime, owns its page ID and `genro.rpc`, and releases pending work.
  The initial WSK default is configurable through PageConfiguration, PageWorker
  and WebpageApplication (`rpc_http_method`), through startup.rpc.httpMethod, and
  with the CLI `--rpc-http-method`. Per-call options.httpMethod wins.
- All integration JS/CSS moved from resources to js/src (one authoritative copy).
  Stable asset URLs are unchanged. Wheel force-include produces the package's
  resources directory. Wheel and sdist built locally; every JS/CSS asset in the
  wheel byte-compared against source; sdist includes js/src. A complete dependency
  bundle and no-sibling installation remain roadmap work, not demonstrated here.
- Registered startup creates genro before opening the core WSX page channel and
  acquiring source; it mounts after receiving a typed SourceBag. Inspector uses
  the same RPC service. An explicit configured HTTP default can fetch source via
  HTTP after opening the channel. The unregistered standalone test/demo retains
  an explicit GET path. No synthetic empty mounted builder is used.
- Remote recipe and inspector handlers validate page/connection/user ownership
  on every call, including GET and POST. Registered page selection is authoritative;
  a caller cannot use the selector to change a registered page's recipe.
- Native browser WebSocket, core 0.43.1: WSX:// JSON envelopes with TYTX JSON data.
  Hosted JSON/MessagePack source replies both verified. MessagePack selection does
  not make the outer WebSocket wire binary. No reconnect, replay, freeze/resume,
  iframe multiplexing or unsolicited server event handling claimed in this phase.
- Correlation, out-of-order replies, HTTP/WSK errors, timeout, late result and
  disposal tests pass. Review found a swallowed mount error: generic mount cleanup
  made the bootstrap look obsolete. Fixed by distinguishing explicit cancellation
  (AbortError) from a failed mount; a malformed Python SourceBag now produces a
  visible startup error. Independent re-review found no remaining concrete bug.
- Real worker-pool test checks two pages, JSON and MessagePack source acquisition,
  HTTP alternatives, missing identity and foreign connection denial. Browser CUA
  on http://127.0.0.1:8014/ demonstrated Hello World binding, MessagePack rebuild,
  textBox second-example isolation, inspector open/close, and playground live
  title plus XML data update. No login required. The inspector button was verified;
  keyboard shortcut remains covered by existing automated runtime tests.
- Live server launch: PYTHONPATH=src:../genro-builders/src:../genro-bag/src:../genro-tytx/src
  temp/registered-startup-venv/bin/python -m genro_pages --modules .. --port 8014
  --state-dir /tmp/genro-pages-channel. PID 62778, worker PID 62789 at launch.
  This uses the same isolated core 0.43.1 environment recorded in phase 1.

Final phase-2 automated verification: 92 pages tests passed in 26.88 seconds;
131 DOM tests passed (including its commit hook). Ruff and diff whitespace checks
passed. DOM dependency checkpoint: 718acbe on codex/python-js-alignment.
