# Project Instructions — genro-pages

**Parent document:** [meta-genro-modules instructions](../../CLAUDE.md).
All general policies are inherited from that document.

## Project context

- Status: Alpha; minimal Hello World integration, no complete page framework.
- Purpose: Python-authored reactive pages using genro-builders, genro-asgi
  and genro-dom-js, with DOM construction and reactivity in the client.
- Preserve legacy recipe names and parameter meanings for migration.
- The Python recipe -> client runtime boundary must be demonstrated by tests;
  do not describe it as implemented until that integration exists.
- genro-ws-web is reference material, not a source of runtime code to copy blindly.
- Existing server GUI work is exploratory. It does not constrain the eventual
  framework or settle a temporary frontend technology.
- Changes to sibling libraries belong to those repositories; do not vendor them.
- Use develop as the integration base. main is the stable branch.
- Code and documentation are in English. Do not add attribution or co-author markers.

Read README.md for scope, then [architecture decisions](docs/architecture/decisions.md)
and the [experiment handoff](docs/architecture/handoff.md) before continuing work.
The architecture record was explicitly requested by the owner for continuity.
Distinguish recorded user requirements from proposed implementation contracts.
New architecture drafts start in temp/ and require review under parent policy.

Before authoring or changing GUI pages, read [GUI 2.0 authoring guide](docs/gui-2.0-guide.md).
Maintain it as the separate record of the owner's agreed GUI conventions;
keep pending API compatibility checks distinct from implemented behavior.

## Dependency consolidation

The owner prefers released dependencies over experimental worktrees. Track missing
behavior in the owning repository, consolidate and release there, then verify
Pages against the released artifact before removing the override. Do not silently
promote branches or substitute local patches for a documented release. See
[dependency consolidation](docs/dependency-consolidation.md) for the current audit.
