const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

function app(search = '') {
    const input = { value: '100' };
    const document = {
        readyState: 'loading',
        addEventListener() {},
        getElementById(id) { return id === 'page-size' ? input : null; }
    };
    const context = vm.createContext({ URLSearchParams, window: { location: { search } }, document, console });
    for (const file of ['utils.js', 'url-state.js', 'app.js']) {
        vm.runInContext(fs.readFileSync(path.join(__dirname, '../docs', file), 'utf8'), context);
    }
    return { context, input };
}

test('invalid sort settings fall back to a supported column and direction', () => {
    for (const column of ['"', 'missing', 'number"][' ]) {
        const { context } = app('?sort=' + encodeURIComponent(column) + '&dir=sideways');
        const state = context.loadStateFromURL();
        assert.equal(state.sortColumn, 'number');
        assert.equal(state.sortDirection, 'asc');
    }
});

test('valid sorting and legacy combined status links retain their meaning', () => {
    const { context } = app('?sort=prize&dir=desc&status=proved%20(Lean)&page=2&pageSize=50');
    const state = context.loadStateFromURL();
    assert.equal(state.sortColumn, 'prize');
    assert.equal(state.sortDirection, 'desc');
    assert.equal(state.statusFilter, 'proved');
    assert.equal(state.formalFilter, 'Lean');
    assert.equal(state.page, 2);
    assert.equal(state.pageSize, 50);
});

for (const value of ['0', '-1', '1.5', '1e3', '9007199254740993', '9'.repeat(400)]) {
    test('URL pagination rejects invalid or unsafe integers: ' + value.slice(0, 20), () => {
        const { context } = app('?page=' + value + '&pageSize=' + value);
        const state = context.loadStateFromURL();
        assert.equal(state.page, 1);
        assert.equal(state.pageSize, 100);
    });
    test('page size input keeps the last valid value: ' + value.slice(0, 20), () => {
        const { context, input } = app();
        input.value = value;
        assert.equal(context.getPageSizeFromUI(), 100);
    });
}

test('large safe page sizes remain supported', () => {
    const { context, input } = app('?pageSize=10000');
    assert.equal(context.loadStateFromURL().pageSize, 10000);
    input.value = '10000';
    assert.equal(context.getPageSizeFromUI(), 10000);
});
