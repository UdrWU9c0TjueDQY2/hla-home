(() => {
  'use strict';

  const rows = document.getElementById('tracker-rows');
  if (!rows) return;

  const locationInput = document.getElementById('kit-location');
  const dateInput = document.getElementById('review-date');
  const addButton = document.getElementById('add-row');
  const prepareButton = document.getElementById('prepare-review');
  const clearButton = document.getElementById('clear-review');
  const output = document.getElementById('tracker-output');
  const summary = document.getElementById('review-summary');
  const copyButton = document.getElementById('copy-summary');
  const downloadButton = document.getElementById('download-csv');
  const printButton = document.getElementById('print-list');
  const fallback = document.getElementById('csv-fallback');
  const csvText = document.getElementById('csv-text');
  const status = document.getElementById('tracker-status');
  const MAX_ROWS = 20;
  let preparedRevision = -1;
  let revision = 0;

  const clean = value => String(value || '').replace(/\s+/g, ' ').trim();
  const safeCsvCell = value => {
    const v = clean(value);
    const guarded = /^[=+\-@\uFF1D\uFF0B\uFF0D\uFF20]/u.test(v) ? `[text] ${v}` : v;
    return `"${guarded.replace(/"/g, '""')}"`;
  };

  function setStatus(message) {
    status.textContent = message;
  }

  function invalidate(message = '') {
    revision += 1;
    preparedRevision = -1;
    output.hidden = true;
    summary.value = '';
    csvText.value = '';
    fallback.hidden = true;
    if (message) setStatus(message);
  }

  function rowData(tr) {
    const fields = tr.querySelectorAll('input, textarea');
    return {
      item: clean(fields[0].value),
      label: clean(fields[1].value),
      date: clean(fields[2].value),
      action: clean(fields[3].value)
    };
  }

  function currentItems() {
    return [...rows.querySelectorAll('tr')].map(rowData).filter(row => Object.values(row).some(Boolean));
  }

  function updateRowControls() {
    const allRows = [...rows.querySelectorAll('tr')];
    allRows.forEach((tr, index) => {
      tr.querySelector('.row-number').textContent = String(index + 1);
      const remove = tr.querySelector('.remove-row');
      remove.disabled = allRows.length === 1;
      remove.setAttribute('aria-label', `Remove row ${index + 1}`);
    });
    addButton.disabled = allRows.length >= MAX_ROWS;
  }

  function addRow(values = {}) {
    if (rows.children.length >= MAX_ROWS) return;
    const tr = document.createElement('tr');
    tr.innerHTML = `<td><label class="small" for="kit-item-${revision}-${rows.children.length}">Item <span class="row-number"></span></label><input id="kit-item-${revision}-${rows.children.length}" autocomplete="off" data-field="item" placeholder="Example: 2 water pouches"></td><td><label class="small" for="kit-label-${revision}-${rows.children.length}">Exact label wording</label><input id="kit-label-${revision}-${rows.children.length}" autocomplete="off" data-field="label" placeholder="Example: best before"></td><td><label class="small" for="kit-date-${revision}-${rows.children.length}">Date as shown</label><input id="kit-date-${revision}-${rows.children.length}" autocomplete="off" data-field="date" placeholder="Example: 2028 MR"></td><td><label class="small" for="kit-action-${revision}-${rows.children.length}">Next action</label><textarea id="kit-action-${revision}-${rows.children.length}" data-field="action" placeholder="Example: check instructions by 15 May"></textarea></td><td class="remove-cell"><button class="tracker-btn danger remove-row" type="button">Remove</button></td>`;
    const fields = tr.querySelectorAll('input, textarea');
    fields[0].value = values.item || '';
    fields[1].value = values.label || '';
    fields[2].value = values.date || '';
    fields[3].value = values.action || '';
    fields.forEach(field => field.addEventListener('input', () => invalidate('List changed. Prepare the summary again when ready.')));
    tr.querySelector('.remove-row').addEventListener('click', () => {
      if (rows.children.length === 1) return;
      tr.remove();
      updateRowControls();
      invalidate('Row removed. Prepare the summary again when ready.');
    });
    rows.append(tr);
    updateRowControls();
  }

  function buildSummary(items) {
    const location = clean(locationInput.value) || 'Not recorded';
    const reviewed = clean(dateInput.value) || 'Not recorded';
    const lines = [
      'EMERGENCY KIT REVIEW LIST',
      `Kit or container: ${location}`,
      `Date reviewed: ${reviewed}`,
      '',
      ...items.flatMap((item, index) => [
        `${index + 1}. Item and quantity: ${item.item || 'Not recorded'}`,
        `   Label wording: ${item.label || 'Not recorded'}`,
        `   Date shown on label: ${item.date || 'Not recorded'}`,
        `   Next action or question: ${item.action || 'Not recorded'}`,
        ''
      ]),
      'Scope: This summary records the entries above. It does not interpret a label, confirm suitability, identify recalls, verify storage conditions or certify that an emergency kit is complete.'
    ];
    return lines.join('\n').trim();
  }

  function buildCsv(items) {
    const location = clean(locationInput.value);
    const reviewed = clean(dateInput.value);
    const header = ['Kit or container', 'Date reviewed', 'Item and quantity', 'Label wording', 'Date shown on label', 'Next action or question'];
    const body = items.map(item => [location, reviewed, item.item, item.label, item.date, item.action].map(safeCsvCell).join(','));
    return '\uFEFF' + header.map(safeCsvCell).join(',') + '\r\n' + body.join('\r\n') + '\r\n';
  }

  function prepare() {
    const items = currentItems();
    if (!items.length) {
      setStatus('Add at least one item, label, date or next action before preparing the summary.');
      output.hidden = true;
      return;
    }
    summary.value = buildSummary(items);
    csvText.value = buildCsv(items);
    preparedRevision = revision;
    output.hidden = false;
    fallback.hidden = true;
    setStatus(`Prepared ${items.length} review ${items.length === 1 ? 'row' : 'rows'}. Review the result before using it.`);
    summary.focus();
  }

  async function copySummary() {
    if (preparedRevision !== revision || !summary.value) return;
    try {
      await navigator.clipboard.writeText(summary.value);
      if (preparedRevision === revision) setStatus('Summary copied.');
    } catch (_) {
      summary.focus();
      summary.select();
      setStatus('Copy was not available. The full summary is selected for manual copying.');
    }
  }

  function downloadCsv() {
    if (preparedRevision !== revision || !csvText.value) return;
    fallback.hidden = true;
    try {
      const blob = new Blob([csvText.value], { type: 'text/csv;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'family-ready-kit-review.csv';
      a.hidden = true;
      document.body.append(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setStatus('CSV download requested. If it did not start, use the complete CSV text shown below.');
    } catch (_) {
      setStatus('CSV download was not available. The complete CSV text is shown for manual copying.');
    }
    fallback.hidden = false;
  }

  function clearAll() {
    locationInput.value = '';
    dateInput.value = '';
    rows.replaceChildren();
    revision += 1;
    addRow();
    output.hidden = true;
    summary.value = '';
    csvText.value = '';
    fallback.hidden = true;
    preparedRevision = -1;
    setStatus('List cleared from this page.');
    locationInput.focus();
  }

  locationInput.addEventListener('input', () => invalidate('List changed. Prepare the summary again when ready.'));
  dateInput.addEventListener('input', () => invalidate('List changed. Prepare the summary again when ready.'));
  addButton.addEventListener('click', () => {
    addRow();
    invalidate('Blank row added.');
    rows.lastElementChild.querySelector('input').focus();
  });
  prepareButton.addEventListener('click', prepare);
  clearButton.addEventListener('click', clearAll);
  copyButton.addEventListener('click', copySummary);
  downloadButton.addEventListener('click', downloadCsv);
  printButton.addEventListener('click', () => {
    if (preparedRevision !== revision || !summary.value) return;
    window.print();
  });

  addRow();
})();
