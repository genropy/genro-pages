// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import {Bag} from 'genro-bag-js';
import {Application, HtmlBuilder} from 'genro-dom-js';

async function renderPage(transport) {
    try {
        const response = await fetch(`/main?transport=${encodeURIComponent(transport)}`);
        if (!response.ok) { throw new Error(`main: HTTP ${response.status}`); }
        const payload = transport === 'msgpack'
            ? new Uint8Array(await response.arrayBuffer()) : await response.text();
        const source = Bag.fromTytx(payload, transport);
        const builder = new HtmlBuilder('main');
        const root = document.getElementById('root');
        const freshRoot = root.cloneNode(false);
        root.replaceWith(freshRoot);
        document.getElementById('error').hidden = true;
        builder.loadSource(source);
        window.genro = new Application(document.getElementById('root'), builder);
        window.page = builder;
        document.getElementById('source-xml').textContent = builder.source.toXml({pretty: true});
    } catch (error) {
        const message = document.getElementById('error');
        message.hidden = false;
        message.textContent = `Impossibile caricare la pagina: ${error.message}`;
        console.error(error);
    }

}
await renderPage(new URLSearchParams(location.search).get('transport') || 'json');
for (const button of document.querySelectorAll('[data-transport]')) {
    button.addEventListener('click', () => renderPage(button.dataset.transport));
}

document.getElementById('source-inspector').addEventListener('toggle', () => {
    if (window.page) {
        document.getElementById('source-xml').textContent = window.page.source.toXml({pretty: true});
    }
});
