/* Navigator behaviour. The needle turns to the bearing of the open page (shortest way round, on a spring),
   the ring fills with scroll depth through that page, the dock stows while reading down and returns on the
   first upward move, and the panel is a native <dialog> with a keyboard-first, searchable list. */
(function () {
  var doc = document, root = doc.documentElement;
  var main = doc.querySelector('main'), app = doc.querySelector('.app');
  var panel = doc.querySelector('[data-navigator-panel]');
  var dock = doc.querySelector('.nav-dock');
  var btn = doc.querySelector('[data-navigator-open]');
  var gauge = doc.querySelector('.nav-depth');
  var hintPlace = doc.querySelector('.nav-dock-place');
  if (!panel || !dock || !btn) return;
  var BEAR = JSON.parse(doc.getElementById('nav-data').textContent);   // {id: {bearing, label, n}}
  var ids = Object.keys(BEAR);

  /* ── Needle: cumulative angle, so it always takes the shorter way round ── */
  var cur = null;
  function turn(id) {
    var b = BEAR[id].bearing;
    if (cur === null) {                     // arrival: swing in from beside north and settle
      cur = b === 0 ? 34 : (b > 180 ? 360 : 0);
      btn.style.setProperty('--bearing', cur + 'deg');
      void btn.offsetWidth;
      requestAnimationFrame(function () { setTo(b); });
    } else { setTo(b); }
  }
  function setTo(b) {
    var d = (((b - cur) % 360) + 540) % 360 - 180;
    cur += d;
    btn.style.setProperty('--bearing', cur + 'deg');
  }

  /* ── Depth: scroll progress through the open page, written on the gauge only ── */
  var queued = false;
  function depth() {
    var range = main.scrollHeight - main.clientHeight;
    var d = range > 0 ? Math.min(1, Math.max(0, main.scrollTop / range)) : 0;
    gauge.style.setProperty('--depth', d.toFixed(4));
    queued = false;
  }
  var lastTop = 0;
  main.addEventListener('scroll', function () {
    if (!queued) { queued = true; requestAnimationFrame(depth); }
    var t = main.scrollTop, atEnd = t + main.clientHeight >= main.scrollHeight - 4;
    if (t < 24 || atEnd || t < lastTop - 2) dock.classList.remove('is-stowed');
    else if (t > lastTop + 6) dock.classList.add('is-stowed');
    lastTop = t;
  }, { passive: true });
  window.addEventListener('resize', depth);

  /* ── Panel ── */
  var filter = panel.querySelector('[data-navigator-filter]');
  var results = panel.querySelector('[data-navigator-results]');
  var empty = panel.querySelector('[data-navigator-empty]');
  var items = function () { return [].slice.call(panel.querySelectorAll('[data-nav-item]')).filter(function (e) { return !e.hidden; }); };
  var active = -1;
  function setActive(i) {
    var list = items();
    if (!list.length) { active = -1; return; }
    active = (i + list.length) % list.length;
    panel.querySelectorAll('[data-active]').forEach(function (e) { e.removeAttribute('data-active'); });
    list[active].setAttribute('data-active', '');
    list[active].scrollIntoView({ block: 'nearest' });
  }
  function applyFilter() {
    var q = filter.value.trim().toLowerCase();
    panel.querySelectorAll('[data-nav-item]').forEach(function (e) { e.hidden = q && e.dataset.label.indexOf(q) < 0; });
    panel.querySelectorAll('.nav-group').forEach(function (g) { g.hidden = !g.querySelector('[data-nav-item]:not([hidden])'); });
    empty.hidden = items().length > 0;
    /* A title match outranks a match buried in a description: the first item whose own
       title equals, then starts with, then contains the query gets the cursor. */
    var list = items(), pick = 0;
    if (q) {
      var title = function (e) { return e.querySelector('.nav-item-label').textContent.trim().toLowerCase(); };
      var tiers = [function (t) { return t === q; }, function (t) { return t.indexOf(q) === 0; }, function (t) { return t.indexOf(q) >= 0; }];
      for (var k = 0; k < tiers.length; k++) {
        var hit = list.findIndex(function (e) { return tiers[k](title(e)); });
        if (hit >= 0) { pick = hit; break; }
      }
    }
    setActive(list.length ? pick : -1);
  }
  function open(focusSearch) {
    var d = btn.getBoundingClientRect(), p = app.getBoundingClientRect();
    panel.style.setProperty('--nav-from', Math.round(d.left + d.width / 2 - p.left) + 'px 100%');
    filter.value = ''; applyFilter();
    panel.showModal();
    btn.setAttribute('aria-expanded', 'true');
    if (focusSearch) filter.focus(); else panel.querySelector('.nav-panel-inner').focus();
  }
  function close() { panel.close(); }
  panel.addEventListener('close', function () { btn.setAttribute('aria-expanded', String(panel.open)); });

  var pressed = '', coarse = window.matchMedia('(pointer: coarse)');
  btn.addEventListener('pointerdown', function (e) { pressed = e.pointerType; });
  btn.addEventListener('click', function (e) {
    var tapped = pressed ? pressed !== 'mouse' : coarse.matches && e.detail > 0;
    pressed = ''; open(!tapped);
  });
  panel.addEventListener('click', function (e) { if (e.target === panel) close(); });
  filter.addEventListener('input', applyFilter);
  panel.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
    else if (e.key === 'Enter') { var t = items()[active]; if (t) { e.preventDefault(); t.click(); } }
  });
  doc.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); panel.open ? close() : open(true); }
  });

  /* ── Going somewhere: a page (tab) and optionally a card inside it ── */
  function show(id, cardId) {
    window.__go(id);
    if (cardId) {
      var el = doc.getElementById(cardId);
      if (el) {
        el.scrollIntoView({ block: 'center', behavior: 'smooth' });
        el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
      }
    }
  }
  results.addEventListener('click', function (e) {
    var a = e.target.closest('[data-nav-item]'); if (!a) return;
    e.preventDefault(); close();
    setTimeout(function () { show(a.dataset.page, a.dataset.card || ''); }, 30);
  });
  doc.querySelectorAll('.pager a').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); show(a.dataset.page, ''); });
  });

  /* Called by the page script after every tab switch. */
  window.__navSync = function (id) {
    turn(id);
    if (hintPlace) hintPlace.textContent = BEAR[id].label;
    btn.setAttribute('aria-label', 'فتح التنقل. أنت الآن في: ' + BEAR[id].label);
    panel.querySelectorAll('.nav-group[data-group="pages"] [data-nav-item]').forEach(function (e) {
      if (e.dataset.page === id) e.setAttribute('aria-current', 'page'); else e.removeAttribute('aria-current');
    });
    dock.classList.remove('is-stowed'); lastTop = 0;
    requestAnimationFrame(depth);
  };
  if (window.__navPending) window.__navSync(window.__navPending);
})();
