# genro-pages

Reactive pages built with Python and Genro.

## Status

**Pre-Alpha — repository seed.** Packaging, documentation and development
configuration are present. No page runtime or test server is implemented yet.
This repository is local; remote hosting and publishing are not configured.

## Purpose

Build live pages from Python recipes, rendered in the browser by genro-dom-js.
An application can host many pages, each with a client source Bag, datastore
and a corresponding server context.

| Project | Responsibility |
| --- | --- |
| genro-builders | Grammars and Python recipe construction |
| genro-dom-js | Client DOM construction and reactivity |
| genro-asgi | Server, routing, transports and resident application contexts |
| genro-pages | Integration of page authoring, bootstrap, recipes and client runtime |

The Python-to-client recipe integration is to be verified, not assumed to work.

## Direction

- Keep source and data as distinct live Bags in the browser.
- Preserve legacy recipe names and parameter meanings where possible to ease migration.
- Support reusable Python and JavaScript components and project-owned web components.
- Obtain the initial recipe through a main call; prefer WebSockets for subsequent
  operations and push updates to a live page context.
- Support remote recipe fragments and lazy resolvers; immediate-value remote
  resolver consumers remain an explicit compatibility question.
- Use user-sticky server contexts to reuse resident objects across calls.
- Learn from genro-ws-web's page, resource and inspector concepts. Its old
  Python-side reactive HTML patch engine is not the selected client model.

A read-only server monitor is the intended first practical consumer.

## First integration experiment

The next implementation should provide a minimal genro-asgi server and test
pages to verify, separately: a Python recipe rendered in the client, data
bindings, source mutations, server data updates and remote recipe fragments.
An inspector should expose the source Bag and datastore. The bootstrap protocol
and public page API are not defined by this scaffold.

## Development

Python 3.11+; Hatchling packaging; pytest; Ruff; advisory mypy; Sphinx/MyST.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,docs]"
ruff check src/ tests/ docs/conf.py
python -m build
sphinx-build -W -b html docs docs/_build/html
```

`tests/` is reserved for the future suite. At this stage pytest exits with code
5 (no tests collected), which the seed CI reports explicitly.

`package.json` declares a local dependency on the sibling `../genro-dom-js`.
There is no browser entry point, bundle or npm test command yet; serving and
resolving its modules belongs to the first integration experiment.

The repository starts with `main` and `develop`; use `develop` for integration.

## License

Apache License 2.0. Copyright 2025-2026 Softwell S.r.l.
See [LICENSE](LICENSE) and [NOTICE](NOTICE).
