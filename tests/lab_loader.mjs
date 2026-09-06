// Resolve the same local modules as the browser import map for contract tests.
const base = new URL('../../', import.meta.url);
export async function resolve(specifier, context, nextResolve) {
    const aliases = {'genro-tytx': 'genro-tytx/js/src/index.js', 'genro-dom-js': 'genro-dom-js/src/index.js', 'genro-bag-js': 'genro-bag-js/src/index.js'};
    if (aliases[specifier]) {
        return {url: new URL(aliases[specifier], base).href, shortCircuit: true};
    }
    if (specifier.startsWith('/_assets/dom/')) {
        return {url: new URL('genro-dom-js/src/' + specifier.slice('/_assets/dom/'.length), base).href, shortCircuit: true};
    }
    if (specifier.startsWith('/_assets/pages/')) {
        return {url: new URL('../src/genro_pages/resources/' + specifier.slice('/_assets/pages/'.length), import.meta.url).href, shortCircuit: true};
    }
    return nextResolve(specifier, context);
}
