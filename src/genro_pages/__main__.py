# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Run the local Hello World integration: python -m genro_pages --modules PATH."""
import argparse

from genro_asgi import AsgiServer

from .demo import DemoApplication


class Cli:
    """Launch the minimal page server with explicit client source locations."""

    def run(self):
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--modules", required=True)
        parser.add_argument("--host", default="127.0.0.1")
        parser.add_argument("--port", type=int, default=8000)
        options = parser.parse_args()
        server = AsgiServer(applications=[DemoApplication(client_modules=options.modules)])
        server.serve(host=options.host, port=options.port)


if __name__ == "__main__":
    Cli().run()
