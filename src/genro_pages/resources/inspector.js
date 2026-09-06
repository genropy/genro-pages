// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
/** Mount a Python recipe and attach real page Bags without reparenting/copying. */
import {Application} from 'genro-dom-js';
import {Bag} from 'genro-bag-js';
import {GalleryBuilder} from './gallery.js';
import {Shortcuts} from './shortcuts.js';

export function mountInspector(host, source, page) {
    const builder = new GalleryBuilder('inspector');
    builder.loadSource(source);
    const app = new Application(host, builder);
    const shortcuts = new Shortcuts(host.ownerDocument);
    const toggle = () => app.live(() => builder.data.setItem('opened', !builder.data.getItem('opened')));
    shortcuts.register('inspector.toggle', 'ctrl+shift+d', toggle, {allowEditing: true});
    const button = host.querySelector('[data-inspector="toggle"]');
    button.addEventListener('click', toggle);
    const subscriptions = [];
    for (const kind of ['data', 'source']) {
        const bag = page.builder[kind];
        const tree = host.querySelector(`[data-inspector="${kind}"]`);
        tree.storeBag = bag;
        const refresh = () => {
            const path = builder.data.getItem(kind + 'Path');
            const node = path ? bag.getNode(path) : null;
            const value = node?.getValue();
            const text = !node ? 'Select a node' : 'Path: ' + path + '\n' + JSON.stringify({
                value: value instanceof Bag ? '[Bag]' : value,
                attributes: node?.attr,
            }, null, 2);
            if (builder.data.getItem(kind + 'Detail') !== text) {
                app.live(() => builder.data.setItem(kind + 'Detail', text));
            }
        };
        const id = 'inspector-detail-' + kind;
        bag.subscribe(id, {any: refresh});
        subscriptions.push(() => bag.unsubscribe(id));
        builder.data.subscribe(id, {any: refresh});
        subscriptions.push(() => builder.data.unsubscribe(id));
    }
    return {app, shortcuts, dispose() {
        shortcuts.dispose();
        subscriptions.forEach(dispose => dispose());
        button.removeEventListener('click', toggle);
        host.replaceChildren();
    }};
}
