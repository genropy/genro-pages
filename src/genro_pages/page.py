# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Python page recipes, independent of their ASGI host."""


class WebPage:
    """Subclass with ordinary Python inheritance."""

    def main(self, root):
        """Populate the source tree."""
        raise NotImplementedError
