# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Run the local Hello World integration: python -m genro_pages --modules PATH."""
import argparse

from genro_asgi import AsgiServer

from .server_configuration import PageConfiguration


class Cli:
    """Launch the minimal page server with explicit client source locations."""

    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--modules", required=True)
        parser.add_argument("--host", default="127.0.0.1")
        parser.add_argument("--port", type=int, default=8000)
        parser.add_argument("--state-dir", help="Worker state directory (default: /tmp/genro-pages-PORT)")
        options = parser.parse_args()
        configuration = PageConfiguration(options.modules, options.state_dir or f"/tmp/genro-pages-{options.port}")
        server = AsgiServer(config=configuration)
        server.serve(host=options.host, port=options.port)


if __name__ == "__main__":
    Cli().run()
