## Phase 1

The owner approved execution and a separate DOM baseline checkpoint.
DOM baseline: 3ef702a; all 128 existing tests passed before implementation.
The baseline preserves prior widget, layout, recipe and topic work; it is not part of this phase.

Supporting file: DOM src/target-wrapper.js records text-node ownership and refuses
in-flight full/partial delivery after disposal. This is necessary to meet the
approved no-resurrection and caller-host ownership requirements; it adds no public API.
A first fixture using explicit HTML IDs exposed the existing distinction between
HTML IDs and generated patch target IDs. The ownership tests use generated IDs,
as the existing writeback tests do; explicit-ID patching is outside this phase.

Implementation dependency: genro-dom-js 4ccf4f2 (baseline 3ef702a).
The owner accepted all proposed names. No naming markers remain.

Read-only review found two reentrancy gaps: component rule batches could run a
second controller after the first disposed the Application; an in-flight full
render could remount after disposal inside a component body. Dispatch and target
delivery now honor disposal, including per-patch checks. Both reproductions are
in the behavioral fixture. Retained Bags remain readable and mutable without
owned reactive effects; external subscriptions remain active. Caller hosts and
replacement Applications are preserved. Child-runtime disposal does not close
its parent. Parent-owned tool/experiment wiring is deliberately Phase 2.

Validation: 3 ownership contract tests; full pages suite 71 passed; DOM 128 passed;
ruff check tests/test_runtime_disposal.py passed; diff whitespace checks passed.
Plan contract fields and original contract skeletons are unchanged. Tests use
real JS DOM/Bag/builder objects; the full pages suite also retains Python/TYTX
JSON and MessagePack integration coverage. No live-browser UI changes in Phase 1.

## Phase 2

Owner approved the execution scope including Application.dispose calling the real genro.dev owner. No generic lifecycle/plugin framework is introduced.

Implementation complete: genro.dev owns the mounted inspector and playground;
Application disposal closes that owner. Inspector teardown now uses Bag's required
{any: true} unsubscribe selector. Laboratory reset disposes only its old experiment.
Bootstrap checks request generation and captured instance after asynchronous steps.

Validation: full pages suite 74 passed; DOM 128 passed; ruff check src tests passed.
Three new consumer contracts run against real Python/TYTX recipes in JSON and
MessagePack. Controlled delayed inspector responses cover both page replacement
and explicit page disposal while waiting. Existing nested tabs and inspector
remount regressions remain green. Original skeleton names/comments are unchanged.

Browser check on localhost: initial example rendered with CodeMirror; two rebuilds
worked; Ctrl+Shift+D opened one inspector; switching to MessagePack preserved one
working inspector and updated navigation transport. No browser errors. Human
Verify remains the authored judgment of familiar interaction and unchanged look.
