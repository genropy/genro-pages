import assert from 'node:assert/strict';
import {setupDom} from '../../genro-dom-js/tests/dom.js';
setupDom();
const {Application} = await import('genro-dom-js');
const {GalleryBuilder} = await import('../src/genro_pages/resources/gallery.js');
class Page extends GalleryBuilder {
    main(root) {
        root.data('title', 'Hello');
        const pane = root.div({datapath:'nested'});
        pane.data('.title', 'Astra');
        pane.span('^.title');
    }
}
const host = document.createElement('div'); document.body.append(host);
const app = new Application(host, new Page('main'));
assert.equal(app.builder.data.getItem('title'), 'Hello');
assert.equal(host.querySelector('span').textContent, 'Astra');
assert.equal(host.querySelector('data'), null);
