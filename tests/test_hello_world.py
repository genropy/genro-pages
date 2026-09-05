# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Contract: ASGI serves a typed Python recipe that the real JS runtime builds."""
import json
import os
from pathlib import Path
import subprocess

import pytest
from genro_asgi import AsgiServer
from genro_bag import Bag

from genro_pages.hello_world import HelloWorldPage


class TestHelloWorld:
    async def request(self, server, path, method="GET", query=b""):
        messages = []

        async def receive():
            return {"type": "http.request", "body": b"", "more_body": False}

        async def send(message):
            messages.append(message)

        await server({"type": "http", "method": method, "path": path,
                      "query_string": query, "headers": []}, receive, send)
        return messages[0], b"".join(m.get("body", b"") for m in messages[1:])

    @property
    def modules(self):
        return Path(os.environ.get("GENRO_CLIENT_MODULES", Path(__file__).resolve().parents[2]))

    @pytest.mark.parametrize("transport", ["json", "msgpack"])
    @pytest.mark.asyncio
    async def test_recipe_crosses_asgi_and_builds_in_javascript(self, transport):
        server = AsgiServer(applications=[HelloWorldPage(client_modules=self.modules)])
        response, body = await self.request(server, "/main", query=f"transport={transport}".encode())
        assert response["status"] == 200
        assert f"application/vnd.tytx+{transport}".encode() in dict(response["headers"])[b"content-type"]
        recipe = Bag.from_tytx(body if transport == "msgpack" else body.decode(), transport=transport)
        if transport == "msgpack":
            assert not body.startswith(b"{")
        assert recipe.get_node("div_0.h1_0").node_tag == "h1"
        assert recipe["div_0.h1_0"] == "Hello World"
        script = Path(__file__).with_name("render_recipe.mjs")
        result = subprocess.run(["node", str(script), str(self.modules), transport], input=body,
                                capture_output=True, check=True)
        rendered = json.loads(result.stdout)
        assert rendered == {"heading": "Hello World", "order": ["H1", "P", "P", "INPUT"],
                            "hidden": False, "readonly": True, "tabindex": 2,
                            "sourceNode": True, "ownership": True}

    @pytest.mark.asyncio
    async def test_shell_and_assets_are_served_without_server_rendering(self):
        server = AsgiServer(applications=[HelloWorldPage(client_modules=self.modules)])
        response, body = await self.request(server, "/")
        assert response["status"] == 200
        assert b'<div id="root" aria-live="polite"></div>' in body
        assert b"<h1>" not in body
        response, body = await self.request(server, "/_assets/dom/index.js")
        assert response["status"] == 200
        assert b"Application" in body
        for path in ("/_assets/dom/../../package.json", "/_assets/missing/index.js"):
            response, _ = await self.request(server, path)
            assert response["status"] == 404
