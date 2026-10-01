/* ===========================================
   PRICE LISTS BY COLART — directory data + rendering
   Add a new business by adding one object to ITEMS below.
   No other markup/code changes are needed.
=========================================== */

const ACCENTS = ['#642878', '#c81478', '#50a0b4', '#64a08c', '#8cb43c', '#dcdc3c'];

const ITEMS = [
  {
    name: 'Joseph Farah',
    slug: 'josephfarah',
    category: 'Beauty & Grooming',
    logo: 'josephfarah/assets/img/josephfarah-logo.svg',
    href: '/josephfarah/'
  },
  {
    name: 'Pearl Beauty Lounge',
    slug: 'pearl-beauty-lounge',
    category: 'Beauty & Grooming',
    logo: 'pearl-beauty-lounge/assets/img/pearl-logo-black.png',
    href: '/pearl-beauty-lounge/'
  }
];

(function () {
  const cardGrid = document.getElementById('cardGrid');
  const toolbar = document.getElementById('toolbar');
  const emptyState = document.getElementById('emptyState');
  const heroCount = document.getElementById('heroCount');
  const searchInput = document.getElementById('searchInput');

  let activeCategory = 'all';
  let query = '';

  function initials(name) {
    return name
      .split(/\s+/)
      .filter(Boolean)
      .slice(0, 2)
      .map(function (w) { return w[0].toUpperCase(); })
      .join('');
  }

  function accentFor(index) {
    return ACCENTS[index % ACCENTS.length];
  }

  function buildChips() {
    const categories = Array.from(new Set(ITEMS.map(function (i) { return i.category; })));
    const frag = document.createDocumentFragment();

    const allChip = document.createElement('button');
    allChip.type = 'button';
    allChip.className = 'chip is-active';
    allChip.textContent = 'All';
    allChip.dataset.category = 'all';
    frag.appendChild(allChip);

    categories.forEach(function (cat) {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'chip';
      chip.textContent = cat;
      chip.dataset.category = cat;
      frag.appendChild(chip);
    });

    toolbar.appendChild(frag);

    toolbar.addEventListener('click', function (e) {
      const btn = e.target.closest('.chip');
      if (!btn) return;
      activeCategory = btn.dataset.category;
      toolbar.querySelectorAll('.chip').forEach(function (c) {
        c.classList.toggle('is-active', c === btn);
      });
      render();
    });
  }

  function cardMarkup(item, index) {
    const accent = accentFor(index);
    const logoInner = item.logo
      ? '<img src="' + item.logo + '" alt="" loading="lazy">'
      : '<span class="initials">' + initials(item.name) + '</span>';

    return (
      '<a class="card" href="' + item.href + '" style="--accent:' + accent + '" aria-label="' + item.name + ': view price list">' +
        '<span class="card-connector"><span class="dot"></span><span class="line"></span></span>' +
        '<span class="card-avatar"><span class="card-avatar-inner">' + logoInner + '</span></span>' +
        '<div class="card-body">' +
          '<div class="card-name">' + item.name + '</div>' +
          '<div class="card-cat">' + item.category + '</div>' +
          '<div class="card-status"><i class="fa-solid fa-circle"></i> View Price List</div>' +
        '</div>' +
        '<span class="card-arrow"><i class="fa-solid fa-arrow-right"></i></span>' +
      '</a>'
    );
  }

  function render() {
    const q = query.trim().toLowerCase();
    const filtered = ITEMS.filter(function (item) {
      const matchesCategory = activeCategory === 'all' || item.category === activeCategory;
      const matchesQuery = !q || item.name.toLowerCase().indexOf(q) !== -1 || item.category.toLowerCase().indexOf(q) !== -1;
      return matchesCategory && matchesQuery;
    });

    cardGrid.innerHTML = filtered.map(function (item) {
      return cardMarkup(item, ITEMS.indexOf(item));
    }).join('');

    emptyState.classList.toggle('is-visible', filtered.length === 0);

    heroCount.innerHTML = '<strong>' + filtered.length + '</strong> price list' + (filtered.length === 1 ? '' : 's');
  }

  searchInput.addEventListener('input', function (e) {
    query = e.target.value;
    render();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
  });

  buildChips();
  render();
})();
