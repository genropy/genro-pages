# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Serve a browser shell and a Python-authored source through genro-asgi.

A WebpageApplication subclass defines main(root). Each main request builds a
fresh HtmlBuilder source and serializes it with Bag.to_tytx; the client loads
that source into genro-dom-js. This first experiment supports root mounting
and ordinary HTML recipes, without per-user state or a WebSocket transport.
"""
from pathlib import Path

from genro_asgi import Response, RoutedApplication
from genro_builders.contrib.html.html_builder import HtmlBuilder
from genro_routes import route


class WebpageApplication(RoutedApplication):
    """Common server counterpart for one recipe-authored page application."""

    mount = ""

    def __init__(self, *, client_modules, **kwargs):
        super().__init__(**kwargs)
        if self.mount != "":
            raise ValueError("This experiment requires root mounting")
        modules = Path(client_modules).resolve()
        self.resources = Path(__file__).parent / "resources"
        self.client_roots = {
            "dom": modules / "genro-dom-js" / "src",
            "bag": modules / "genro-bag-js" / "src",
            "tytx": modules / "genro-tytx" / "js" / "src",
            "pages": self.resources,
        }
        for directory in self.client_roots.values():
            if not directory.is_dir():
                raise ValueError(f"Missing client source directory: {directory}")

    def main(self, root):
        """Populate the recipe; override in the concrete page."""
        raise NotImplementedError

    @route(name="main", media_type="application/vnd.tytx+json")
    def get_main(self):
        """Return the typed source recipe, without rendering HTML in Python."""
        builder = HtmlBuilder("main")
        self.main(builder.source)
        return builder.source.to_tytx()

    @route(media_type="text/html")
    def index(self):
        """Return the browser bootstrap shell."""
        return (self.resources / "index.html").read_text()

    async def __call__(self, scope, receive, send):
        path = scope.get("path", "")
        if scope["type"] == "http" and path.startswith("/_assets/"):
            if scope.get("method") not in ("GET", "HEAD"):
                await Response("Method not allowed", status_code=405)(scope, receive, send)
                return
            parts = path.removeprefix("/_assets/").split("/", 1)
            directory = self.client_roots.get(parts[0])
            target = (directory / parts[1]).resolve() if directory and len(parts) == 2 else None
            if (target is None or not target.is_relative_to(directory.resolve())
                    or target.suffix != ".js" or not target.is_file()):
                await Response("Not found", status_code=404)(scope, receive, send)
                return
            content = b"" if scope.get("method") == "HEAD" else target.read_bytes()
            await Response(content, media_type="text/javascript")(scope, receive, send)
            return
        await super().__call__(scope, receive, send)
