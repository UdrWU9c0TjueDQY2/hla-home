const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');

const path = process.argv[2] || 'src/roommend/wall-paint-area-calculator/index.html';
const html = fs.readFileSync(path, 'utf8');
const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)].map(x => x[1]);
const source = scripts.find(x => x.includes('const kind="paint"'));
assert(source, 'actual calculator script found');

class Element {
  constructor(value = '') { this.value = value; this.defaultValue = value; this.textContent = ''; this.innerHTML = ''; this.disabled = false; this.hidden = false; this.events = {}; }
  addEventListener(type, fn) { this.events[type] = fn; }
  fire(type) { return this.events[type]?.({ preventDefault() {} }); }
  get innerText() { return this.innerHTML.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim(); }
  checkValidity() {
    const n = Number(this.value);
    return this.value !== '' && Number.isFinite(n) && n >= this.min && n <= this.max && (this.step !== 1 || Number.isInteger(n));
  }
}
const values = { length: '4', width: '3', height: '2.4', openings: '4', coats: '2', coverage: '10', units: 'metric' };
const els = Object.fromEntries(Object.entries(values).map(([k, v]) => [k, new Element(v)]));
for (const id of ['result', 'detail', 'visual', 'copy', 'status', 'inputs', 'restore']) els[id] = new Element();
const fields = ['length', 'width', 'height', 'openings', 'coats', 'coverage'];
for (const id of fields) Object.assign(els[id], { min: id === 'openings' ? 0 : id === 'coats' ? 1 : 0.1, max: id === 'openings' ? 100000 : id === 'coats' ? 10 : id === 'height' ? 100 : id === 'coverage' ? 10000 : 1000, step: id === 'coats' ? 1 : .01 });
const writes = [];
let clipboardImpl = text => { writes.push(text); return Promise.resolve(); };
const document = { title: 'Wall Paint Area Calculator: Room Size, Openings and Coats', getElementById: id => els[id], querySelectorAll: selector => { assert.equal(selector, '#inputs input'); return fields.map(id => els[id]); } };
function HTMLFormElement() {}
HTMLFormElement.prototype.reset = function () { for (const [k, value] of Object.entries(values)) els[k].value = value; };
vm.runInNewContext(source, { document, navigator: { clipboard: { writeText: text => clipboardImpl(text) } }, location: { href: 'https://example.test/tool/#test' }, HTMLFormElement });
const change = (id, value) => { els[id].value = value; return els.inputs.fire('input'); };
const copy = () => els.copy.fire('click');

(async () => {
  assert.equal(els.result.textContent, '5.92 L estimated');
  assert.equal(els.copy.disabled, false);
  await copy();
  assert.match(writes[0], /5\.92 L estimated/);
  assert.match(writes[0], /33\.60 m² walls − 4\.00 m² openings = 29\.60 m²/);
  assert.match(els.status.textContent, /Copied/);
  const firstWrites = writes.length;
  change('length', '');
  assert.equal(els.copy.disabled, true, 'invalid edit must disable Copy');
  assert.equal(els.status.textContent, '', 'invalid edit clears prior status');
  await copy();
  assert.equal(writes.length, firstWrites, 'guard refuses validation-error payload');

  for (const [id, value] of [['length', '-1'], ['length', 'Infinity'], ['length', '1001'], ['coats', '1.5'], ['coverage', '0'], ['openings', '100']]) {
    els.restore.fire('click');
    change(id, value);
    assert.equal(els.copy.disabled, true, id + '=' + value + ' invalid');
    const before = writes.length;
    await copy();
    assert.equal(writes.length, before);
  }

  els.restore.fire('click');
  assert.equal(els.copy.disabled, false, 'valid restore enables Copy');
  assert.equal(els.status.textContent, '');
  change('openings', '33.6');
  assert.equal(els.result.textContent, '0.00 L estimated');
  assert.equal(els.copy.disabled, false, 'zero paintable area is valid');

  els.restore.fire('click');
  clipboardImpl = () => Promise.reject(new Error('denied'));
  await copy();
  assert.match(els.status.textContent, /Copy unavailable/);
  change('units', 'us');
  assert.equal(els.status.textContent, '', 'unit edit clears failure');
  assert.match(els.result.textContent, /US gal/);

  let finish;
  clipboardImpl = text => { writes.push(text); return new Promise(resolve => { finish = resolve; }); };
  const pending = copy();
  change('length', '5');
  finish();
  await pending;
  assert.equal(els.status.textContent, '', 'late success must not describe changed input');

  let fail;
  clipboardImpl = () => new Promise((_, reject) => { fail = reject; });
  const lateFailure = copy();
  change('coverage', '');
  fail(new Error('late'));
  await lateFailure;
  assert.equal(els.status.textContent, '', 'late failure must not replace validation state');
  assert.equal(els.copy.disabled, true);
  console.log('RoomMend paint: 13 handler/lifecycle groups passed');
})().catch(error => { console.error(error); process.exitCode = 1; });
