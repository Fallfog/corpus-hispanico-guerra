(() => {
  const input = document.querySelector('#archive-search');
  const category = document.querySelector('#archive-category');
  const period = document.querySelector('#archive-period');
  if (!input || !category || !period) return;
  const cards = [...document.querySelectorAll('#archive-grid .article-card')];
  const empty = document.querySelector('#no-results');
  const counter = document.querySelector('#results-count');
  const norm = v => String(v || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
  const params = new URLSearchParams(location.search);
  category.value = params.get('categoria') || '';
  input.value = params.get('q') || '';
  period.value = params.get('periodo') || '';
  function apply() {
    const q = norm(input.value); let count = 0;
    for (const card of cards) {
      const show = (!q || norm(card.dataset.search).includes(q)) &&
        (!category.value || card.dataset.cat === category.value) &&
        (!period.value || card.dataset.period === period.value);
      card.hidden = !show;
      if (show) count++;
    }
    empty.hidden = count !== 0;
    counter.textContent = `${count} ${count === 1 ? 'FICHA' : 'FICHAS'} EN EL ARCHIVO`;
  }
  for (const el of [input, category, period]) el.addEventListener(el === input ? 'input' : 'change', apply);
  apply();
})();
