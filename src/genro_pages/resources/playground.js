// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import {bagXmlView} from './bag-xml-view.js';
import {LabSession, INITIAL_CODE, CHANGE_CODE} from './lab-session.js';

export async function mountPlayground(host, ui) {
    const builder = ui.builder;
    const node = id => host.querySelector('[data-lab="' + id + '"]');
    // Each mounted Application owns its input events, including nested previews.
    for (const type of ['input', 'change']) {
        host.addEventListener(type, event => event.stopPropagation());
        node('lab-preview').addEventListener(type, event => event.stopPropagation());
    }
    const set = (path, value) => ui.live(() => builder.data.setItem(path, value));
    set('code', INITIAL_CODE);
    const session = new LabSession(node('lab-preview'), current => {
        ui.live(() => {
            builder.data.setItem('dataXml', bagXmlView(current.app.builder.data, 'data'));
            builder.data.setItem('sourceXml', bagXmlView(current.app.builder.source, 'source'));
        });
    });
    const rebuild = () => {
        try { session.reset(node('lab-code').value); set('status', 'Example rebuilt from code.'); }
        catch (error) { set('status', `${error.name}: ${error.message}`); }
    };
    node('lab-rebuild').onclick = rebuild;
    node('lab-apply').onclick = () => {
        try { session.run(node('lab-code').value); set('status', 'Code applied to the current Bags.'); }
        catch (error) { set('status', `${error.name}: ${error.message} (changes already applied are retained)`); }
    };
    node('lab-example').onclick = () => {
        set('code', CHANGE_CODE);
        set('status', 'Example loaded: click Apply to current example.');
    };
    node('lab-reset').onclick = () => {
        session.reset();
        set('code', INITIAL_CODE);
        set('status', 'Initial example restored.');
    };
    node('lab-code').addEventListener('focusout', event => {
        if (!builder.data.getItem('auto') || node('lab-code').contains(event.relatedTarget)) { return; }
        if (node('lab-toolbar').contains(event.relatedTarget)) { return; }
        rebuild();
    });
    return {ui, session};
}
