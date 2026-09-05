// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
// Behavioral bridge: input comes from the real ASGI /main response.
import {pathToFileURL} from 'node:url';
import {readFileSync} from 'node:fs';
const base = pathToFileURL(`${process.argv[2]}/`);
const {Bag} = await import(new URL('genro-bag-js/src/index.js', base));
const {setupDom} = await import(new URL('genro-dom-js/tests/dom.js', base));
const {Application, HtmlBuilder, SourceBagNode} = await import(new URL('genro-dom-js/src/index.js', base));
setupDom();
const builder = new HtmlBuilder('main');
const transport = process.argv[3] || 'json';
builder.loadSource(Bag.fromTytx(transport === 'msgpack' ? readFileSync(0) : readFileSync(0, 'utf8'), transport));
const root = document.createElement('div');
const app = new Application(root, builder);
const node = builder.source.getNode('div_0.h1_0');
console.log(JSON.stringify({
    heading: root.querySelector('h1').textContent,
    order: [...root.firstElementChild.children].map(n => n.tagName),
    hidden: root.firstElementChild.hidden,
    readonly: root.querySelector('input').readOnly,
    tabindex: root.querySelector('input').tabIndex,
    sourceNode: node instanceof SourceBagNode,
    ownership: node.builder === builder && node.handler === app.handler,
}));
