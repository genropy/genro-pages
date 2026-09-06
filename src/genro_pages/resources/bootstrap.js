// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import {Bag} from 'genro-bag-js';
import {Application, HtmlBuilder} from 'genro-dom-js';
import {fromTytx} from 'genro-tytx';
import {highlightRecipes} from './recipe-highlight.js';
import {mountInspector} from './inspector.js';
let generation = 0;

export async function renderPage(transport) {
    const ticket = ++generation;
    let app;
    const current = () => ticket === generation && !app?._disposed;
    try {
        const query = new URLSearchParams({transport});
        const selected = new URLSearchParams(location.search).get('page');
        document.getElementById("source-inspector").hidden = selected === "playground";
        if (selected !== null) { query.set('page', selected); }
        const response = await fetch(`/main?${query}`);
        if (!response.ok) { throw new Error(`main: HTTP ${response.status}`); }
        const payload = transport === 'msgpack'
            ? new Uint8Array(await response.arrayBuffer()) : await response.text();
        if (!current()) return;
        const source = fromTytx(payload, transport);
        const Builder = selected === 'playground'
            ? (await import('./playground-page.js')).PlaygroundBuilder
            : selected?.startsWith('widgets/')
            ? (await import('./gallery.js')).GalleryBuilder : HtmlBuilder;
        if (!current()) return;
        const builder = new Builder('main');
        const root = document.getElementById('root');
        const freshRoot = root.cloneNode(false);
        window.genro?.dispose();
        root.replaceWith(freshRoot);
        document.getElementById('error').hidden = true;
        builder.loadSource(source);
        app = new Application(freshRoot, builder);
        window.genro = app;
        window.page = builder;
        const inspectorResponse = await fetch('/inspector');
        if (!current()) return;
        if (!inspectorResponse.ok) throw new Error('Inspector: HTTP ' + inspectorResponse.status);
        const inspectorSource = fromTytx(await inspectorResponse.text(), 'json');
        if (!current()) return;
        mountInspector(document.getElementById('developer-tools'), inspectorSource, app);
        if (selected === "playground") {
            const {mountPlayground} = await import("./playground.js");
            if (!current()) return;
            await mountPlayground(freshRoot, app);
        }
        if (!current()) return;
        void highlightRecipes(freshRoot);
        document.getElementById('source-xml').textContent = builder.source.toXml({pretty: true});
    } catch (error) {
        if (!current()) return;
        const message = document.getElementById('error');
        message.hidden = false;
        message.textContent = `Unable to load the page: ${error.message}`;
        console.error(error);
    }

}
async function renderMenu(transport) {
    const response = await fetch(`/menu?transport=${encodeURIComponent(transport)}`);
    if (response.status === 404) { return; }
    if (!response.ok) { throw new Error(`menu: HTTP ${response.status}`); }
    const payload = transport === 'msgpack'
        ? new Uint8Array(await response.arrayBuffer()) : await response.text();
    const source = Bag.fromTytx(payload, transport);
    function entries(bag) {
        const list = document.createElement('ul');
        for (const node of bag) {
            const item = document.createElement('li');
            if (node.nodeTag === 'branch') {
                const label = document.createElement('span');
                label.textContent = node.attr.label;
                item.append(label, entries(node.value));
            } else if (node.nodeTag === 'webpage') {
                const link = document.createElement('a');
                const query = new URLSearchParams({page: node.attr.filepath, transport});
                link.href = `/?${query}`;
                link.textContent = node.attr.label;
                item.append(link);
            }
            list.append(item);
        }
        return list;
    }
    document.getElementById('page-menu').replaceChildren(entries(source));
}
const transport = new URLSearchParams(location.search).get('transport') || 'json';
await renderPage(transport);
try {
    await renderMenu(transport);
} catch (error) {
    const message = document.getElementById('error');
    message.hidden = false;
    message.textContent = `Unable to load the menu: ${error.message}`;
}
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

document.getElementById('source-inspector').addEventListener('toggle', () => {
    if (window.page) {
        document.getElementById('source-xml').textContent = window.page.source.toXml({pretty: true});
    }
});
