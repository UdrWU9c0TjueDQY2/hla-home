'use strict';

const names = ['Household contacts', 'Insurance records', 'Home documents', 'Care instructions'];
const steps = [
  'Agree where the current copy belongs.',
  'Clarify who may access it with the record owner.',
  'Check whether the copy is current.'
];
const $ = id => document.getElementById(id);
const printButton = $('print-result');

function invalidate() {
  $('result').textContent = '';
  printButton.disabled = true;
}

for (let i = 0; i < 4; i += 1) {
  const skip = $('skip' + i);
  skip.addEventListener('change', () => {
    for (let k = 0; k < 3; k += 1) $('g' + i + 's' + k).disabled = skip.checked;
    invalidate();
  });
  for (let k = 0; k < 3; k += 1) $('g' + i + 's' + k).addEventListener('change', invalidate);
}

$('review').addEventListener('click', () => {
  const lines = [];
  let used = 0;
  for (let i = 0; i < 4; i += 1) {
    if ($('skip' + i).checked) continue;
    used += 1;
    const missing = [];
    for (let k = 0; k < 3; k += 1) {
      if (!$('g' + i + 's' + k).checked) missing.push(steps[k]);
    }
    lines.push(names[i] + ': ' + (missing.length ? missing.join(' ') : 'All three checks marked done.'));
  }
  $('result').textContent = used
    ? lines.join('\n\n') + '\n\nThis records your choices only. It does not verify documents or assess emergency readiness.'
    : 'All categories are marked not applicable. No categories were assessed.';
  printButton.disabled = used === 0;
});

printButton.addEventListener('click', () => {
  if (!printButton.disabled) window.print();
});

$('reset').addEventListener('click', () => {
  for (let i = 0; i < 4; i += 1) {
    $('skip' + i).checked = false;
    for (let k = 0; k < 3; k += 1) {
      const field = $('g' + i + 's' + k);
      field.checked = false;
      field.disabled = false;
    }
  }
  invalidate();
});
