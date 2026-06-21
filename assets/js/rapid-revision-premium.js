(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Scroll reveal */
  function initReveal() {
    var targets = document.querySelectorAll(".rr-bento__cell, .pg-price-card");
    if (!targets.length) return;

    if (reduceMotion || !("IntersectionObserver" in window)) {
      targets.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );

    targets.forEach(function (el, i) {
      el.style.transitionDelay = i * 0.08 + "s";
      observer.observe(el);
    });
  }

  /* Mode compare tabs (registration hub) */
  function initModeTabs() {
    var tabs = document.querySelectorAll(".rr-mode-tab");
    if (!tabs.length) return;

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        var mode = tab.getAttribute("data-mode");
        tabs.forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
        });
        document.querySelectorAll(".rr-mode-panel").forEach(function (panel) {
          panel.classList.toggle("is-active", panel.getAttribute("data-panel") === mode);
        });
        document.querySelectorAll(".rr-mode-card").forEach(function (card) {
          card.classList.remove("is-highlighted");
        });
        var highlight = document.querySelector('.rr-mode-card[data-mode="' + mode + '"]');
        if (highlight) highlight.classList.add("is-highlighted");
      });
    });
  }

  /* Tier pills (payment pages) */
  function initTierPills() {
    var pills = document.querySelectorAll(".rr-tier-pill");
    if (!pills.length) return;

    pills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        var tier = pill.getAttribute("data-tier");
        pills.forEach(function (p) {
          p.classList.toggle("is-active", p === pill);
        });
        document.querySelectorAll(".pg-price-card").forEach(function (card) {
          card.classList.remove("is-spotlight");
        });
        var target = document.getElementById("tier-" + tier);
        if (target) {
          target.classList.add("is-spotlight");
          if (!reduceMotion) {
            target.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
        }
      });
    });

    if (pills.length) {
      var defaultPill = document.querySelector('.rr-tier-pill[data-tier="group"]') || pills[0];
      defaultPill.click();
    }
  }

  /* FAQ accordion */
  function initFaq() {
    document.querySelectorAll(".rr-faq__trigger").forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        var item = trigger.closest(".rr-faq__item");
        var isOpen = item.classList.contains("is-open");
        item.parentElement.querySelectorAll(".rr-faq__item").forEach(function (i) {
          i.classList.remove("is-open");
        });
        if (!isOpen) item.classList.add("is-open");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      initReveal();
      initModeTabs();
      initTierPills();
      initFaq();
    });
  } else {
    initReveal();
    initModeTabs();
    initTierPills();
    initFaq();
  }
})();
