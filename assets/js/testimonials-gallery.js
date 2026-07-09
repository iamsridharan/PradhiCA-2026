/**
 * PradhiCA — Testimonials gallery interactions
 * Filters, progressive reveal, lightbox, keyboard nav
 */
(function () {
  'use strict';

  var PAGE_SIZE = 24;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var masonry = document.getElementById('tmon-masonry');
  var countEl = document.getElementById('tmon-visible-count');
  var moreWrap = document.getElementById('tmon-more');
  var moreBtn = document.getElementById('tmon-load-more');
  var filterBtns = document.querySelectorAll('.tmon-filter');

  var lb = document.getElementById('tmon-lb');
  var lbImg = document.getElementById('tmon-lb-img');
  var lbCaption = document.getElementById('tmon-lb-caption');
  var lbClose = document.getElementById('tmon-lb-close');
  var lbPrev = document.getElementById('tmon-lb-prev');
  var lbNext = document.getElementById('tmon-lb-next');

  if (!masonry) return;

  var allCards = Array.prototype.slice.call(masonry.querySelectorAll('.tmon-card'));
  var activeFilter = 'all';
  var shownLimit = PAGE_SIZE;
  var lbIndex = 0;
  var lastFocus = null;
  var revealObserver = null;

  function matchingCards() {
    return allCards.filter(function (card) {
      return activeFilter === 'all' || card.getAttribute('data-batch') === activeFilter;
    });
  }

  function visibleCards() {
    return matchingCards().filter(function (card) {
      return !card.classList.contains('is-hidden');
    });
  }

  function updateCount() {
    var matched = matchingCards().length;
    var visible = visibleCards().length;
    var suffix = document.getElementById('tmon-count-suffix');
    if (countEl) {
      countEl.textContent = String(visible);
    }
    if (suffix) {
      if (visible < matched) {
        suffix.textContent = 'of ' + matched + ' stories';
      } else if (activeFilter === 'all') {
        suffix.textContent = 'stories showing';
      } else {
        suffix.textContent = 'stories in this attempt';
      }
    }
    if (moreWrap) {
      if (visible < matched) {
        moreWrap.hidden = false;
      } else {
        moreWrap.hidden = true;
      }
    }
  }

  function applyVisibility() {
    var matched = matchingCards();
    allCards.forEach(function (card) {
      var match = activeFilter === 'all' || card.getAttribute('data-batch') === activeFilter;
      var idxInMatch = matched.indexOf(card);
      var withinLimit = idxInMatch > -1 && idxInMatch < shownLimit;
      if (match && withinLimit) {
        card.classList.remove('is-hidden');
      } else {
        card.classList.add('is-hidden');
        card.classList.remove('is-in');
      }
    });
    updateCount();
    observeCards();
  }

  function observeCards() {
    if (reduceMotion) {
      visibleCards().forEach(function (card) {
        card.classList.add('is-in');
      });
      return;
    }
    if (revealObserver) {
      revealObserver.disconnect();
    }
    revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { rootMargin: '0px 0px -8% 0px', threshold: 0.12 }
    );
    visibleCards().forEach(function (card, i) {
      if (card.classList.contains('is-in')) return;
      card.style.transitionDelay = Math.min(i % 8, 7) * 0.05 + 's';
      revealObserver.observe(card);
    });
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var filter = btn.getAttribute('data-filter') || 'all';
      activeFilter = filter;
      shownLimit = PAGE_SIZE;
      filterBtns.forEach(function (b) {
        var on = b === btn;
        b.classList.toggle('is-active', on);
        b.setAttribute('aria-selected', on ? 'true' : 'false');
      });
      applyVisibility();
    });
  });

  if (moreBtn) {
    moreBtn.addEventListener('click', function () {
      shownLimit += PAGE_SIZE;
      applyVisibility();
    });
  }

  /* ---------- Lightbox ---------- */
  function openLb(index) {
    var cards = matchingCards();
    if (!cards.length) return;
    lbIndex = ((index % cards.length) + cards.length) % cards.length;
    var card = cards[lbIndex];
    var link = card.querySelector('[data-lb-src]');
    if (!link) return;
    var src = link.getAttribute('data-lb-src');
    var label = link.getAttribute('data-lb-label') || 'Story';
    lastFocus = document.activeElement;
    lbImg.src = src;
    lbImg.alt = 'PradhiCA student success message - ' + label;
    lbCaption.textContent = label + ' · ' + (lbIndex + 1) + ' / ' + cards.length;
    lb.hidden = false;
    lb.classList.add('is-open');
    document.body.classList.add('tmon-lb-lock');
    if (lbClose) lbClose.focus();
  }

  function closeLb() {
    lb.classList.remove('is-open');
    document.body.classList.remove('tmon-lb-lock');
    window.setTimeout(function () {
      if (!lb.classList.contains('is-open')) {
        lb.hidden = true;
        lbImg.removeAttribute('src');
      }
    }, 400);
    if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
  }

  function stepLb(delta) {
    openLb(lbIndex + delta);
  }

  masonry.addEventListener('click', function (e) {
    var link = e.target.closest('[data-lb-src]');
    if (!link) return;
    e.preventDefault();
    var card = link.closest('.tmon-card');
    var cards = matchingCards();
    var idx = cards.indexOf(card);
    if (idx < 0) idx = 0;
    openLb(idx);
  });

  if (lbClose) lbClose.addEventListener('click', closeLb);
  if (lbPrev) lbPrev.addEventListener('click', function () { stepLb(-1); });
  if (lbNext) lbNext.addEventListener('click', function () { stepLb(1); });

  lb.addEventListener('click', function (e) {
    if (e.target === lb) closeLb();
  });

  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      closeLb();
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      stepLb(-1);
    } else if (e.key === 'ArrowRight') {
      e.preventDefault();
      stepLb(1);
    }
  });

  /* Touch swipe on lightbox */
  var touchX = null;
  if (lb) {
    lb.addEventListener(
      'touchstart',
      function (e) {
        if (e.changedTouches && e.changedTouches[0]) {
          touchX = e.changedTouches[0].clientX;
        }
      },
      { passive: true }
    );
    lb.addEventListener(
      'touchend',
      function (e) {
        if (touchX === null || !e.changedTouches || !e.changedTouches[0]) return;
        var dx = e.changedTouches[0].clientX - touchX;
        touchX = null;
        if (Math.abs(dx) < 48) return;
        stepLb(dx > 0 ? -1 : 1);
      },
      { passive: true }
    );
  }

  applyVisibility();
})();
