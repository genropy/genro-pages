// Copyright 2026 Softwell S.r.l. - SPDX-License-Identifier: Apache-2.0
import {Application} from 'genro-dom-js';
import {RpcService} from './rpc.js';

/** Python-page integration; the standalone DOM library knows nothing of RPC. */
export class PageApplication extends Application {
    // wf:phase-2:new
    constructor(rootElement, startup) {
        super(rootElement);
        this.pageId = startup.getItem('page_id');
        this.rpc = new RpcService(this, startup.getItem('rpc'));
    }

    // wf:phase-2:new
    dispose() {
        this.rpc?.dispose();
        super.dispose();
    }
}
