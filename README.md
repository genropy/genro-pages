# genro-pages

Reactive pages built with Python and Genro.

## Status

**Alpha — first integration experiment.** A minimal genro-asgi server returns
an HtmlBuilder source through TYTX; genro-dom-js constructs it in the browser.
This is an ordinary-HTML Hello World, not a complete page framework.

## Hello World

The class hierarchy is `RoutedApplication -> WebpageApplication -> HelloWorldPage`.
The concrete page defines `main(root)`. The common base serves an empty browser
shell at `/`, the typed recipe at `/main`, and explicitly configured JS sources
at `/_assets/`. The browser retains its source Bag and datastore.

Use the matching `codex/python-js-alignment` branches of genro-bag-js and
genro-dom-js, plus genro-tytx commit `80529f7`. They must be sibling folders under
the directory passed as `--modules`. genro-tytx may be a symlink to its checkout.
Install Python dependencies in the chosen environment, then from this repository:

```sh
PYTHONPATH=src python -m genro_pages --modules .. --port 8010
```

Open http://127.0.0.1:8010/. The disclosure below the page shows the mounted JavaScript source Bag as XML,
using `builder.source.toXml({pretty: true})`. It refreshes when opened. `window.genro` and `window.page`
expose the client runtime and source builder for inspection.

The command launches a native ASGI application in the genro-asgi worker pool
(requires genro-asgi 0.43.1). Each valid HTML request registers a toolbox-generated
22-character page ID before embedding it in the TYTX startup Bag. The core emits
the connection cookie. The source still travels over HTTP until the next startup
phase; registration alone does not imply the client uses WebSocket yet.

Worker state defaults to `/tmp/genro-pages-PORT`; use `--state-dir` to select another
short local path (Unix socket paths have a length limit). The direct application
constructor used by isolated recipe tests still supports unregistered rendering.
The current local builder 0.23.2 is required and is not yet available from PyPI.

The server is mounted at the site root and binds to loopback by default. The
source-directory asset server is intended for this local experiment; bundled
asset distribution is not implemented. Only `.js` and `.mjs` files beneath the configured
roots are served.

## Validation

```sh
PYTHONPATH=src python -m pytest tests/
ruff check src/ tests/
```

The integration test calls the real AsgiServer, sends its `/main` output to the
JS runtime under jsdom, and checks nesting/order, text, typed attributes and
source ownership. It requires Node and the sibling DOM repository's jsdom dev
dependency. Set `GENRO_CLIENT_MODULES` if the client repositories are elsewhere.
The second test checks the empty shell, asset serving and path confinement.

See [the experiment record](docs/hello-world.md) for exact dependency commits,
the command used locally and browser observations.

## Next steps

Preserve browser reactivity and legacy recipe names. This experiment does not
implement initial datastore transport, per-user/page residency, WebSocket calls,
remote fragments, resolver transport or component-body transport. Datastore root
semantics remain under review in genro-builders issue #37; Hello World does not
change them. Existing JS web-component collections remain available for the next
experiment, but this page uses ordinary HTML only.

## License

Apache License 2.0. Copyright 2025-2026 Softwell S.r.l.
See LICENSE and NOTICE.

## MessagePack comparison

The page has JSON and MessagePack buttons. `/main?transport=msgpack` returns
`application/vnd.tytx+msgpack` bytes. The browser reads an ArrayBuffer, calls
`Bag.fromTytx(new Uint8Array(buffer), 'msgpack')`, then loads the decoded source
through the same builder. The inspector shows the mounted source Bag as XML after decoding and activation;
it is not the network payload.

The Python environment needs `genro-tytx[msgpack]`; the client source checkout
needs `@msgpack/msgpack` in `genro-tytx/js/node_modules` (tested with 3.1.3).
The browser shim maps TYTX's lazy requires to the existing ESM codec and the
library's ESM distribution. No MessagePack codec is copied into pages.

Three integration cases pass: JSON and MessagePack both build the expected DOM,
plus shell/asset checks. Both transports were observed in the in-app browser.
