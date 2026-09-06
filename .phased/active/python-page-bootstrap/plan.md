# Context: codex/hello-world
Parent: develop
Mode: interactive
Channel: in-chat
Must not break: Python page recipes remain typed SourceBags transported through TYTX JSON and MessagePack and rendered in the browser.
Must not break: every Application owns an independent rooted data Bag; source-node context, relative paths and genro.dev cleanup survive page replacement.
Must not break: obsolete asynchronous page/tool responses cannot revive disposed instances or mutate replacement controls.
Must not break: future RPC and iframe integration consumes real server identity; no fabricated page_id, socket topology or ready/onStart contract is introduced here.
Must not break: the existing gallery, laboratory, inspector shortcut, menu destinations, CSS appearance and mobile viewport remain available.

## Objective

Generate the initial HTML document through the Python HtmlBuilder and transmit an
explicit startup configuration as a TYTX Bag, separate from the later source
recipe. Select the JavaScript builder and optional setup through Python page
metadata, removing URL-name special cases from generic startup. This is the
approved document/configuration slice of Macro 3; registered identity and
readiness remain a separate ASGI integration block.

## Work Plan

- [>] **Phase 1**: Generate the page document and drive startup from typed configuration
  > In execution since 2026-09-06T19:48:58.833405+00:00
  > Testing: awaiting the human's `Verify: now` checks | commit: 2957c11
  - Run: opus / high
  - Pattern: sibling `genro-builders/tests/test_html_attrs.py:_render` verifies `HtmlBuilder.create()` and `render(target=False)`; `tests/test_hello_world.py:RequestSupport` and `tests/test_runtime_consumers.py:TestRuntimeOwnership._check` exercise ASGI responses and real Python/TYTX recipes in JavaScript.
  - Files: new `src/genro_pages/page_document.py`; `src/genro_pages/application.py`, `page.py`, `widget_test_page.py`, `pages/playground.py`; `resources/bootstrap.js`, new `resources/shell.css`, replace/remove the obsolete static `resources/index.html`; existing `resources/gallery.js`, `playground-page.js` and `playground.js` only if metadata integration requires it; new `tests/test_page_bootstrap.py` and JS fixture, `tests/test_hello_world.py`, `tests/test_runtime_consumers.py`, `tests/runtime_consumers.mjs`; `docs/gui-2.0-guide.md`, `docs/architecture/runtime-reorganization-plan.md`.
  - Decisions: use `PageDocument(HtmlBuilder)` with `build_head`, `build_body`, `build_menu` methods and ordinary Python composition/docstrings. Page classes declare `client_builder` and optional `client_setup` as module/export pairs; default builder is the existing HtmlBuilder, widget pages use GalleryBuilder and playground uses PlaygroundBuilder plus mountPlayground. Preserve existing exported names and setup(host, application) calling convention. The server derives configuration from registered classes, never a query-supplied module. Configuration is a Bag serialized with TYTX JSON embedded as inert script data; source recipes retain selectable JSON/MessagePack transport. No Mako, new dependency, artificial identity or ready event. Keep existing route/query entry points and legacy one-page Application.main subclass support. Move shell CSS unchanged into its own asset; preserve theme order, import map, document language, viewport and existing host IDs. No UI redesign.
  - Details: build exactly one HTML5 document with doctype, head and body; keep the page's main recipe out of the initial body. Resolve and validate selected/default page and transport on the server. Put the selected route, transport, existing endpoint/host configuration, builder/setup descriptors and existing development-view visibility into the startup Bag. Defaults for source inspection come from page metadata/configuration, not route spelling. Safely embed both startup payload and import-map JSON: the existing HtmlRenderer treats script/style bodies as raw text, so HTML text escaping alone cannot prevent a literal closing script tag. Preserve typed values and Unicode after extraction/decoding. Build navigation with the document builder from the existing validated menu Bag; include the same branch/webpage destinations, preserve query encoding, and keep the /menu endpoint compatible. Generic JS startup consumes the configuration, imports the declared builder/setup, then uses the existing generation and captured-Application guards around every awaited step. Transport switches continue to dispose old instances and update menu links. Preserve inspector and laboratory ownership through genro.dev. Adapt the bootstrap integration fixture to use real Python-generated shell/configuration rather than its current handwritten HTML. No source edits in sibling libraries are planned; if HtmlBuilder cannot meet a required contract, report the concrete missing capability rather than working around it with a second HTML renderer.
  - Done: the plan's tests for this phase, copied into the test tree with skeleton bodies implemented, pass. Run `PYTHONPATH=src:../genro-builders/src:../genro-bag/src:../genro-tytx/src python -m pytest tests/` and `ruff check src tests`; sibling genro-dom-js `npm test` remains green. Verify document structure and configuration by parsing actual ASGI HTML and decoding it with the real JS TYTX implementation; cover adversarial text including closing script tags, quotes, ampersands and Unicode. Prove arbitrary registered route names select their declared builder/setup without bootstrap edits, in both transports. Preserve all existing ownership/remount/late-response scenarios; do not weaken their assertions when replacing handwritten shell fixtures. Exercise browser startup, menu navigation, transport switching, laboratory rebuild and Ctrl+Shift+D with no console errors. Contract tests inspect observable behavior, not only source-text patterns.
  - Verify: now — view Hello World, one widget page and the laboratory; confirm the layout and familiar interaction are unchanged after moving document construction to Python.

## Boundaries and rationale

One phase is appropriate because document generation and its configuration
consumer form one deployable, verifiable result; neither half is useful alone.
Mode and channel were explicitly selected: interactive, in this conversation.
The owner approved the proposed scope and names with permission to revisit them
if implementation evidence warrants it. That does not authorize speculative APIs.
This is a refactor preserving appearance, not a new visual-design phase.

Later consumers are recipe compatibility/RPC, server identity and root/iframe
transport. Their inherited contracts appear above; they must not infer page
registration, full subtree lifecycle or readiness from this slice. The server
identity integration requires checking actual ASGI code and ratified decisions,
not assuming that the dated websocket design document describes deployed code.

## Starting state and references

Adopt existing branch codex/hello-world; no new checkout, merge or push.
Pages starting revision cafb0a1; DOM dependency f743e6c. Both were clean at planning.
Prior workflow: `.phased/done/page-owned-runtime/plan.md`.
Legacy evidence: `docs/architecture/runtime-legacy-contract.md`, Verified HTML
construction paths (PageTemplate/HeaderTemplate and startup argument preparation).
Current shell: `WebpageApplication.index` reads resources/index.html. Current JS
chooses builders and playground setup by route strings. Existing renderMenu makes
DOM directly; its Bag vocabulary and destinations are retained by build_menu.
ASGI pages contract read at planning is version 0.4 in the reference repository;
it requires HTTP-created page identity before openchannel. No ASGI API is consumed
by this plan beyond the current HTTP application/response integration.
