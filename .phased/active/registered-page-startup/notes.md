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
