// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import {Application, HtmlBuilder} from 'genro-dom-js';

try {
    const response = await fetch('/main', {headers: {'Accept': 'application/vnd.tytx+json'}});
    if (!response.ok) { throw new Error(`main: HTTP ${response.status}`); }
    const payload = await response.text();
    document.getElementById('payload').textContent = payload;
    const builder = new HtmlBuilder('main');
    builder.loadSource(payload); // Bag.fromTytx uses genro-tytx inside the existing runtime.
    window.genro = new Application(document.getElementById('root'), builder);
    window.page = builder;
} catch (error) {
    const message = document.getElementById('error');
    message.hidden = false;
    message.textContent = `Impossibile caricare la pagina: ${error.message}`;
    console.error(error);
}
