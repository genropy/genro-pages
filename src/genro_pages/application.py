# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Host registered Python page recipes and a static Bag menu.

Each source request instantiates its selected page and a fresh HtmlBuilder.
The browser owns DOM construction and reactivity. Explicit registration keeps
page identity independent of menu captions and future directory discovery.
Subclass main(root) remains supported for the original one-page experiment.
"""
from pathlib import Path

from genro_asgi import HTTPBadRequest, HTTPNotFound, Response, RoutedApplication
from genro_builders.contrib.html.html_builder import HtmlBuilder
from genro_routes import route
from genro_tytx import to_tytx


class WebpageApplication(RoutedApplication):
    """ASGI host for explicitly registered recipe-authored pages."""

    mount = ""

    def __init__(self, *, client_modules, pages=None, menu_class=None, default_page=None, **kwargs):
        super().__init__(**kwargs)
        if self.mount != "":
            raise ValueError("This experiment requires root mounting")
        self.pages = dict(pages or {})
        self.menu_class = menu_class
        self.default_page = default_page
        if self.pages and default_page not in self.pages:
            raise ValueError("Default page must be registered")
        modules = Path(client_modules).resolve()
        self.resources = Path(__file__).parent / "resources"
        self.client_roots = {
            "dom": modules / "genro-dom-js" / "src",
            "bag": modules / "genro-bag-js" / "src",
            "tytx": modules / "genro-tytx" / "js" / "src",
            "pages": self.resources,
            "msgpack": modules / "genro-tytx" / "js" / "node_modules" / "@msgpack" / "msgpack" / "dist.esm",
        }
        for directory in self.client_roots.values():
            if not directory.is_dir():
                raise ValueError(f"Missing client source directory: {directory}")

    def main(self, root):
        """Populate the recipe; override in the concrete page."""
        raise NotImplementedError

    @route(name="main")
    def get_main(self, transport="json", page=None):
        """Return the typed source recipe, without rendering HTML in Python."""
        if transport not in ("json", "msgpack"):
            raise HTTPBadRequest("Supported transports: json, msgpack")
        if self.pages:
            page_class = self.pages.get(page if page is not None else self.default_page)
            if page_class is None:
                raise HTTPNotFound("Unknown page")
            builder = getattr(page_class, "source_builder", HtmlBuilder)("main")
            page_class().main(builder.source)
        else:
            builder = HtmlBuilder("main")
            if page is not None:
                raise HTTPNotFound("Unknown page")
            self.main(builder.source)
        return self.result_wrapper(
            to_tytx(builder.source, transport=transport),
            media_type=f"application/vnd.tytx+{transport}",
        )

    @route(name="menu")
    def get_menu(self, transport="json"):
        """Return the menu as a typed Bag."""
        if transport not in ("json", "msgpack"):
            raise HTTPBadRequest("Supported transports: json, msgpack")
        if self.menu_class is None:
            raise HTTPNotFound("No menu configured")
        menu = self.menu_class()
        menu.create()
        self.validate_menu(menu.source)
        return self.result_wrapper(menu.source.to_tytx(transport=transport),
                                   media_type=f"application/vnd.tytx+{transport}")

    @route(name="inspector")
    def get_inspector(self):
        """Serve the development tool through the same typed recipe boundary."""
        from .inspector import build_inspector
        from .widget_test_builder import WidgetTestBuilder
        builder = WidgetTestBuilder("inspector")
        build_inspector(builder.source)
        return self.result_wrapper(to_tytx(builder.source, transport="json"),
                                   media_type="application/vnd.tytx+json")

    def validate_menu(self, source):
        """Reject unknown destinations and unsupported vocabulary."""
        for node in source:
            if node.node_tag == "branch":
                self.validate_menu(node.value)
            elif node.node_tag == "webpage":
                if node.attr.get("filepath") not in self.pages:
                    raise ValueError("Menu references an unregistered page")
            else:
                raise ValueError(f"Unsupported menu tag: {node.node_tag}")

    @route(media_type="text/html")
    def index(self, page=None, transport="json"):
        """Serve the shell; the browser forwards page/transport to recipe requests."""
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
                    or target.suffix not in (".js", ".mjs", ".css") or not target.is_file()):
                await Response("Not found", status_code=404)(scope, receive, send)
                return
            content = b"" if scope.get("method") == "HEAD" else target.read_bytes()
            await Response(content, media_type="text/css" if target.suffix == ".css" else "text/javascript")(scope, receive, send)
            return
        await super().__call__(scope, receive, send)
