const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

function item(tag, labelText) {
    const checkbox = { value: tag, className: 'tag-filter-checkbox' };
    const label = { textContent: labelText };
    return {
        style: {},
        querySelector(selector) {
            if (selector === '.tag-filter-checkbox') return checkbox;
            if (selector === 'label') return label;
            return null;
        },
    };
}

function load(items) {
    const document = {
        querySelectorAll() { return items; },
        getElementById() { return null; },
        addEventListener() {},
    };
    const context = vm.createContext({ document, console });
    vm.runInContext(
        fs.readFileSync(path.join(__dirname, '../docs/filters.js'), 'utf8'),
        context,
    );
    return context;
}

test('tag search ignores the count shown next to the name', () => {
    const primes = item('primes', 'primes (10)');
    const powers = item('powers', 'powers (4/12)');
    const context = load([primes, powers]);

    context.filterTagCheckboxes('10');
    assert.equal(primes.style.display, 'none');
    assert.equal(powers.style.display, 'none');

    context.filterTagCheckboxes('pow');
    assert.equal(primes.style.display, 'none');
    assert.equal(powers.style.display, 'flex');

    context.filterTagCheckboxes('');
    assert.equal(primes.style.display, 'flex');
    assert.equal(powers.style.display, 'flex');
});
