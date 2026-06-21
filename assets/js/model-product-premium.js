(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function initReveal() {
    var targets = document.querySelectorAll(".model-price-card");
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
      { threshold: 0.12, rootMargin: "0px 0px -32px 0px" }
    );

    targets.forEach(function (el, i) {
      if (el.classList.contains("model-price-card")) {
        el.style.transitionDelay = i * 0.07 + "s";
      }
      observer.observe(el);
    });
  }

  function initTierPills() {
    var pills = document.querySelectorAll(".model-tier-pill");
    if (!pills.length) return;

    pills.forEach(function (pill) {
      pill.addEventListener("click", function () {
        var tier = pill.getAttribute("data-tier");
        pills.forEach(function (p) {
          p.classList.toggle("is-active", p === pill);
        });
        document.querySelectorAll(".model-price-card").forEach(function (card) {
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

    if (pills[2]) {
      pills[2].click();
    } else if (pills[0]) {
      pills[0].click();
    }
  }

  function initSpotlight() {
    if (reduceMotion) return;

    document.querySelectorAll(".model-price-card").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var rect = card.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width) * 100;
        var y = ((e.clientY - rect.top) / rect.height) * 100;
        card.style.setProperty("--spot-x", x + "%");
        card.style.setProperty("--spot-y", y + "%");
      });
    });
  }

  function boot() {
    initReveal();
    initTierPills();
    initSpotlight();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
