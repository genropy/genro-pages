// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import {Application} from 'genro-dom-js';
import {fromTytx} from 'genro-tytx';
import {highlightRecipes} from './recipe-highlight.js';
import {mountInspector} from './inspector.js';
const startup = fromTytx(document.getElementById('page-startup').textContent, 'json');
const hosts = startup.getItem('hosts');
let generation = 0;

export async function renderPage(transport) {
    const ticket = ++generation;
    let app;
    const current = () => ticket === generation && !app?._disposed;
    try {
        const query = new URLSearchParams({transport});
        const selected = startup.getItem('page');
        document.getElementById(hosts.getItem('inspection')).hidden = !startup.getItem('source_inspection');
        if (selected !== null) { query.set('page', selected); }
        const response = await fetch(`${startup.getItem('endpoints.main')}?${query}`);
        if (!response.ok) { throw new Error(`main: HTTP ${response.status}`); }
        const payload = transport === 'msgpack'
            ? new Uint8Array(await response.arrayBuffer()) : await response.text();
        if (!current()) return;
        const source = fromTytx(payload, transport);
        const client = startup.getItem('client_builder');
        const Builder = (await import(client.getItem('module')))[client.getItem('export')];
        if (!current()) return;
        const builder = new Builder('main');
        const root = document.getElementById(hosts.getItem('root'));
        const freshRoot = root.cloneNode(false);
        window.genro?.dispose();
        root.replaceWith(freshRoot);
        document.getElementById(hosts.getItem('error')).hidden = true;
        builder.loadSource(source);
        app = new Application(freshRoot, builder);
        window.genro = app;
        window.page = builder;
        const inspectorResponse = await fetch(startup.getItem('endpoints.inspector'));
        if (!current()) return;
        if (!inspectorResponse.ok) throw new Error('Inspector: HTTP ' + inspectorResponse.status);
        const inspectorSource = fromTytx(await inspectorResponse.text(), 'json');
        if (!current()) return;
        mountInspector(document.getElementById(hosts.getItem('tools')), inspectorSource, app);
        const setup = startup.getItem('client_setup');
        if (setup) {
            const mount = (await import(setup.getItem('module')))[setup.getItem('export')];
            if (!current()) return;
            await mount(freshRoot, app);
        }
        if (!current()) return;
        void highlightRecipes(freshRoot);
        document.getElementById(hosts.getItem('source')).textContent = builder.source.toXml({pretty: true});
    } catch (error) {
        if (!current()) return;
        const message = document.getElementById(hosts.getItem('error'));
        message.hidden = false;
        message.textContent = `Unable to load the page: ${error.message}`;
        console.error(error);
    }

}
await renderPage(startup.getItem('transport'));
for (const button of document.querySelectorAll('[data-transport]')) {
    button.addEventListener('click', async () => {
        await renderPage(button.dataset.transport);
        for (const link of document.querySelectorAll('#page-menu a')) {
            const url = new URL(link.href);
            url.searchParams.set('transport', button.dataset.transport);
            link.href = url.href;
        }
    });
}

document.getElementById(hosts.getItem('inspection')).addEventListener('toggle', () => {
    if (window.page) {
        document.getElementById(hosts.getItem('source')).textContent = window.page.source.toXml({pretty: true});
    }
});
