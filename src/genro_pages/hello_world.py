# Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
"""The first page: its entire visible content is a Python recipe."""
from .application import WebpageApplication


class HelloWorldPage(WebpageApplication):
    """A nested HTML recipe with text and typed attributes."""

    def main(self, root):
        page = root.div(node_id="hello", class_="hello", hidden=False)
        page.h1("Hello World")
        page.p("Questa pagina è costruita nel browser da una ricetta Python.")
        page.p("Python → TYTX → genro-dom-js", class_="path")
        page.input(value="Genro Pages", readonly=True, tabindex=2)

        experiment = root.div(class_="hello", margin_top="24px")
        experiment.h2("Prova il binding")
        experiment.p("Scrivi un titolo: poi esci dal campo per aggiornare il testo qui sotto.")
        experiment.input(value="^titolo", node_id="title_input",
                         placeholder="Scrivi qui…", aria_label="Titolo")
        experiment.div("^titolo", node_id="title_echo", font_size="28px",
                       min_height="45px", margin_top="16px")
