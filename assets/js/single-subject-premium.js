(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Scroll reveal */
  function initReveal() {
    var targets = document.querySelectorAll(".ss-bento__cell, .pg-price-card, .ss-option-card");
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
    var tabs = document.querySelectorAll(".ss-mode-tab");
    if (!tabs.length) return;

    tabs.forEach(function (tab) {
      tab.addEventListener("click", function () {
        var mode = tab.getAttribute("data-mode");
        tabs.forEach(function (t) {
          t.classList.toggle("is-active", t === tab);
          t.setAttribute("aria-selected", t === tab ? "true" : "false");
        });
        document.querySelectorAll(".ss-mode-panel").forEach(function (panel) {
          panel.classList.toggle("is-active", panel.getAttribute("data-panel") === mode);
        });
        document.querySelectorAll(".ss-mode-card, .ss-option-card").forEach(function (card) {
          card.classList.remove("is-highlighted");
        });
        var highlight = document.querySelector('.ss-mode-card[data-mode="' + mode + '"]');
        if (highlight) highlight.classList.add("is-highlighted");
        filterOptionCards();
      });
    });
  }

  /* Model toggle + option grid (registration hub) */
  function initModelPicker() {
    var modelPills = document.querySelectorAll(".ss-model-pill");
    if (!modelPills.length) return;

    modelPills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        modelPills.forEach(function (p) {
          p.classList.toggle("is-active", p === pill);
        });
        filterOptionCards();
      });
    });

    filterOptionCards();
  }

  function filterOptionCards() {
    var activeModeTab = document.querySelector(".ss-mode-tab.is-active");
    var activeModelPill = document.querySelector(".ss-model-pill.is-active");
    if (!activeModelPill) return;

    var mode = activeModeTab ? activeModeTab.getAttribute("data-mode") : "all";
    var model = activeModelPill.getAttribute("data-model");
    var cards = document.querySelectorAll(".ss-option-card");
    if (!cards.length) return;

    cards.forEach(function (card) {
      var cardMode = card.getAttribute("data-mode");
      var cardModel = card.getAttribute("data-model");
      var modeMatch = mode === "all" || mode === "compare" || cardMode === mode;
      var modelMatch = cardModel === model;
      var show = modeMatch && modelMatch;
      card.classList.toggle("is-dimmed", !show);
      card.classList.toggle("is-highlighted", show && mode !== "all" && mode !== "compare");
    });
  }

  /* Tier pills (payment pages) */
  function initTierPills() {
    var pills = document.querySelectorAll(".ss-tier-pill");
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
      var defaultPill = document.querySelector('.ss-tier-pill[data-tier="group"]') || pills[0];
      defaultPill.click();
    }
  }

  /* FAQ accordion */
  function initFaq() {
    document.querySelectorAll(".ss-faq__trigger").forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        var item = trigger.closest(".ss-faq__item");
        var isOpen = item.classList.contains("is-open");
        item.parentElement.querySelectorAll(".ss-faq__item").forEach(function (i) {
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
      initModelPicker();
      initTierPills();
      initFaq();
    });
  } else {
    initReveal();
    initModeTabs();
    initModelPicker();
    initTierPills();
    initFaq();
  }
})();
