const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

const context = vm.createContext({ document: { createElement() { return {}; } }, console });
vm.runInContext(fs.readFileSync(path.join(__dirname, '../docs/utils.js'), 'utf8'), context);

test('decidable problems use the same AI label as falsifiable and verifiable', () => {
    const problem = { informal_status: { state: 'decidable' } };
    const html = context.renderAIAttempts('19', problem);
    assert.match(html, />view</);
    assert.match(html, /id=19/);
    assert.match(context.renderAIAttempts('23', { informal_status: { state: 'falsifiable' } }), />view</);
    assert.match(context.renderAIAttempts('2', { informal_status: { state: 'proved' } }), />add</);
});
