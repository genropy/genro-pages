
## Phase 1

Execution approved in chat. Implemented the initial PageDocument composition,
startup Bag, page client descriptors, shell stylesheet extraction and generic
bootstrap imports. Contract skeletons copied unchanged; bodies still pending.

Dependency blocker found on first integration run: HtmlBuilder declares
`details` with `sub_tags='summary[0:1]'` in
`../genro-builders/src/genro_builders/contrib/html/html5_elements.py:126`.
Consequently the existing shell's `details > summary + pre` cannot be expressed:
`ValueError: 'pre' not allowed as child of 'details'` from PageDocument.build_body.
`tests/test_hello_world.py`: 4 passed, 3 failed (all initial HTML requests).
No retry, bypass, alternate renderer or sibling edit attempted.

The plan explicitly requires reporting missing builder capabilities. Ask the
owner to authorize a bounded genro-builders correction with its own regression
test (preserving summary cardinality and allowing flow content), then resume
this phase. Existing sibling changes must be preserved. Current implementation
is incomplete: startup requests fail until the grammar is corrected; the demo
has not been restarted. Next: settle the dependency correction; finish six
contract bodies, adapt runtime_consumers fixtures to real generated HTML, run
full suites and browser checks, update docs, and request the authored human QA.
