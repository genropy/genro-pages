
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

### Continuation after issue #39

Owner requested proceeding with the remaining work while the builder issue is
open. No dependency fix was authorized or attempted. Added implementations for
the six immutable contract skeletons, real generated-shell consumption in the
runtime ownership fixture, a Node bootstrap/typed-data fixture and the pages
asset alias in the test loader. Added documentation with explicit pending status.
Typed the optional client_setup descriptor to resolve the earlier mypy advisory.

Validation: 70 existing tests passed, with the 4 existing full-bootstrap cases
explicitly deselected because of #39; the six new full-document contracts have
not been executed while the known prerequisite is absent. DOM suite: 128 passed.
Ruff and JavaScript syntax checks passed. An isolated generated-head check parsed
its actual HTML and decoded startup through JS TYTX, preserving hostile closing
script text, Unicode, date, number and boolean, with no injected DOM. The first
version of that standalone check omitted the Bag module registration; adding
its side-effect import (also in the new fixture) made it pass. Production
bootstrap already imports Application and its Bag dependency.

Next: after #39 lands, run all six contracts and the complete pages suite,
resolve any newly exposed integration defects, exercise the browser, and
complete the authored human Verify check. No completion or browser success is
claimed by this checkpoint.
