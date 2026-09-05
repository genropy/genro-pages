# Hello World experiment

Date: 2026-09-05. Implemented and observed locally; not a general page protocol.

## Dependencies used

| Repository | Commit | Role |
| --- | --- | --- |
| genro-asgi | a434a23d23af000ba87d57491f0035023bed7a5d | Server |
| genro-builders | e4efb187cf0a75efa5e85055ee5279691ae13d9c | Python HtmlBuilder |
| genro-bag | 1b13b1ef15f8caa772275e5329a7e033af11bab4 | Python source serialization |
| genro-tytx | 80529f7a9ef26d8fbfac4c5b52423e9a51818f52 | Python/JS typed codec |
| genro-bag-js | 005b01d | TYTX tag/type alignment |
| genro-dom-js | e5540e0 | Source loading and reactive activation |

The JS repositories are isolated worktrees under
`/Users/gporcari/Documents/ChatGPT/genro-pages/worktrees`. The genro-tytx sibling
there is a symlink to the original checkout. No library code is vendored into
pages. Existing untracked files in the original repositories were not modified.

## Actual local start command

```sh
PYTHONPATH=/Users/gporcari/Documents/ChatGPT/genro-pages/worktrees/genro-pages/src:/Users/gporcari/Sviluppo/genro_ng/meta-genro-modules/sub-projects/genro-builders/src:/Users/gporcari/Sviluppo/genro_ng/meta-genro-modules/sub-projects/genro-bag/src:/Users/gporcari/Sviluppo/genro_ng/meta-genro-modules/sub-projects/genro-tytx/src \
/Users/gporcari/Sviluppo/genro_ng/meta-genro-modules/sub-projects/genro-asgi/.venv/bin/python \
-m genro_pages --modules /Users/gporcari/Documents/ChatGPT/genro-pages/worktrees --port 8010
```

This uses the existing ASGI development environment (Python 3.14); automated
pytest validation additionally ran with Python 3.12.9 and source paths for the
same repositories. JS DOM tests used Node 23.11.0 and jsdom.

## Evidence

The in-app browser loaded http://127.0.0.1:8010/ and displayed Hello World,
two paragraphs and the readonly Genro Pages input. Expanding the recipe
control displayed the server's TYTX rows, including semantic tags, nested
parent paths, `hidden: false`, `readonly: true` and `tabindex: 2`.
The HTML shell contains no h1/content recipe: the visible page is built after
fetching `/main`, calling `loadSource`, and mounting the existing Application.

Two integration tests passed. They verify the actual ASGI response through
jsdom and the real aligned runtime, including SourceBagNode identity and
builder/handler references. The underlying dependency branches separately passed
505 Bag tests, 111 DOM tests and six Python/JS/Python round trips.

The initial sandboxed bind was refused by the OS; the authorized local server
was then started successfully. No deployment or remote push was performed.

## Limits and next experiment

Ordinary HTML and primitive typed attributes only. Each main request constructs
a fresh recipe. No Python-to-JS function transport, websocket page context,
initial data transport, reconnection, remote fragments, resolver transport or
widget-collection integration is claimed. The two client stores retain the
existing JS architecture; the datastore-root question is tracked separately at
https://github.com/genropy/genro-builders/issues/37.

Next: one existing web-component collection and initial data transport, after
confirming datastore root and addressing semantics.
