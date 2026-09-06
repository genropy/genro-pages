# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""Recipe for the development inspector; inspected Bags stay in their owner."""


def build_inspector(root):
    """Compose the launcher, floating shell and two independent tree views."""
    root.data("opened", False)
    root.button("Inspector · Ctrl+Shift+D", **{
        "data-inspector": "toggle", "aria-keyshortcuts": "Control+Shift+D"})
    palette = root.palette(title="Developer tools · Page", value="^opened",
                           width="600px", height="480px", left="90px", top="80px")
    palette.p("Actual page Bags · select a node to inspect its value and attributes.")
    tabs = palette.tabContainer()
    for kind in ("data", "source"):
        build_view(tabs.tab(key=kind, label=kind.title()), kind)


def build_view(pane, kind):
    """Keep the tree and selected-node detail together in each tab."""
    pane.storeTree(selectedPath=f"^{kind}Path", height="250px", overflow="auto",
                   **{"data-inspector": kind})
    pane.data(f"{kind}Detail", "Select a node")
    pane.pre(f"^{kind}Detail", **{"data-inspector": f"{kind}-detail"})
