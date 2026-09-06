# GUI runtime reorganization

Mode: interactive
Channel: in-chat

## Agreed direction

Preserve the legacy authoring mental model with modern, maintainable internals.
Python builds both the bootstrap document (DOM builder, no Mako) and page recipes.
Each page owns genro, a source Bag and one rooted data Bag. Recipe callbacks use
their source node as this where the legacy contract requires it. Modules follow
responsibilities; public collection imports remain stable. English artifacts.

## Macro 1 — Runtime contract (completed)

Starts from the existing experimental gallery and documented partial audit.
Ends at an evidence-backed compatibility matrix, proposed ownership tree and
behavioral scenarios that make the first implementation macro ready to plan.
No production runtime changes. Archived plan: done/runtime-contract/plan.md.

## Macro 2 — Page-owned runtime (first implementation slice completed)

Archived first-slice plan: done/page-owned-runtime/plan.md.

Requires Macro 1's lifecycle, source context, deletion and connection contracts.
Ends at a usable gallery/playground/inspector owned through genro, with isolated
instances and recursive, idempotent cleanup. Detail implementation phases only
after Macro 1 evidence and API proposals have been reviewed.

## Macro 3 — Python-generated bootstrap (document/configuration slice planned)

Active plan: active/python-page-bootstrap/plan.md. Registered identity and
readiness remain separate prerequisites for the full macro outcome.

Requires ownership/readiness from Macro 2 and the approved ASGI identity seam.
Ends at builder-generated HTML and explicit startup configuration, with generic
client startup and recipe-authored laboratory controls. Preserve both TYTX
transports and source/data types. Do not invent registry page IDs.

## Macro 4 — Recipe compatibility

Requires source ownership, startup order and compiler contracts from earlier work.
Ends at verified GET/SET/PUT/FIRE, event connections, topics and data-provider
compatibility for the agreed supported subset. RPC depends on the builder and
ASGI contracts; declaration support alone is not operational RPC.

## Requirements carried through all macros

- Legacy migration: familiar recipe names, relative paths, callback scope and
  parameter meanings; intentional differences documented with concrete reasons.
- Mobile: capability-based pointer handling, usable touch handles, scroll/zoom,
  cancellation and keyboard behavior. Real-device checks remain distinct from
  automated checks. Do not import legacy prototype patches or global suppression.
- ASGI: one physical WebSocket on the root; nested pages have independent identity,
  runtime and cleanup. Parent/child transport routing must not leak page state.
- Data: source/data stay distinct; typed values survive transport. Future selective
  data synchronization must not require mirroring every client dataset on server.
- Existing gallery, inspector and playground remain regression consumers.

Mobile implementation and ASGI integration require later bounded plans. Open
external decisions stay open until the owner records them; mailbox proposals do
not settle them. This roadmap does not authorize speculative facades or new APIs.

The completed first Macro 2 slice establishes Application and tool ownership.
Source-subtree hooks and general connection compatibility still require planning
before declaring the entire macro complete.
