/**
 * CA Final Nov 2026 test schedule — 3D tilt, sticky series rail, tab UX
 */
(function () {
  "use strict";

  var root = document.body;
  if (!root.classList.contains("pg-test-schedule--final-nov26")) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var seriesNav = document.getElementById("ts-series-rail");
  var hero = document.querySelector(".ts-hero");
  var tabLinks = document.querySelectorAll("#ts-series-rail .nav-link[data-toggle='tab']");

  /* —— Sticky series rail shadow when pinned —— */
  if (seriesNav && "IntersectionObserver" in window) {
    var sentinel = document.createElement("div");
    sentinel.className = "ts-series-rail-sentinel";
    sentinel.setAttribute("aria-hidden", "true");
    seriesNav.parentNode.insertBefore(sentinel, seriesNav);

    var railObserver = new IntersectionObserver(
      function (entries) {
        seriesNav.classList.toggle("is-pinned", !entries[0].isIntersecting);
      },
      { rootMargin: "-1px 0px 0px 0px", threshold: 1 }
    );
    railObserver.observe(sentinel);
  }

  /* —— Sync rail indicator + hero quick actions on tab change —— */
  function setActiveSeries(targetId) {
    if (!targetId) return;
    tabLinks.forEach(function (link) {
      var isActive = link.getAttribute("href") === targetId;
      link.classList.toggle("is-current", isActive);
      link.setAttribute("aria-selected", isActive ? "true" : "false");
    });
    document.querySelectorAll(".ts-hero__jump").forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("href") === targetId);
    });
  }

  tabLinks.forEach(function (link) {
    link.addEventListener("shown.bs.tab", function (e) {
      setActiveSeries(e.target.getAttribute("href"));
    });
  });

  /* —— Hero quick-jump pills trigger same tabs —— */
  document.querySelectorAll(".ts-hero__jump[data-toggle='tab']").forEach(function (jump) {
    jump.addEventListener("click", function (e) {
      e.preventDefault();
      var target = jump.getAttribute("href");
      var railLink = document.querySelector('#ts-series-rail .nav-link[href="' + target + '"]');
      if (railLink && typeof jQuery !== "undefined") {
        jQuery(railLink).tab("show");
      }
    });
  });

  /* —— Deep-link hash on load —— */
  if (window.location.hash && document.querySelector(window.location.hash + ".tab-pane")) {
    var hashLink = document.querySelector('#ts-series-rail .nav-link[href="' + window.location.hash + '"]');
    if (hashLink && typeof jQuery !== "undefined") {
      jQuery(hashLink).tab("show");
    }
    setActiveSeries(window.location.hash);
  } else {
    setActiveSeries("#Tabsabc");
  }

  /* —— 3D parallax tilt on feature cards —— */
  if (!reduceMotion) {
    var tiltMax = 8;

    function bindTilt(card) {
      var inner = card.querySelector(".ts-feature-card__inner");
      if (!inner) return;

      card.addEventListener("pointermove", function (e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        var rotateX = (-y * tiltMax).toFixed(2);
        var rotateY = (x * tiltMax).toFixed(2);
        inner.style.transform =
          "rotateX(" + rotateX + "deg) rotateY(" + rotateY + "deg) translateZ(12px)";
        card.style.setProperty("--spot-x", (x * 50 + 50) + "%");
        card.style.setProperty("--spot-y", (y * 50 + 50) + "%");
      });

      card.addEventListener("pointerleave", function () {
        inner.style.transform = "";
      });
    }

    document.querySelectorAll(".ts-feature-card").forEach(bindTilt);

    /* Hero 3D stage follows pointer subtly */
    var stage = document.querySelector(".ts-hero-3d__stage");
    if (stage && hero) {
      hero.addEventListener("pointermove", function (e) {
        var rect = hero.getBoundingClientRect();
        var x = ((e.clientX - rect.left) / rect.width - 0.5) * 14;
        var y = ((e.clientY - rect.top) / rect.height - 0.5) * -10;
        stage.style.transform =
          "rotateX(" + y.toFixed(1) + "deg) rotateY(" + x.toFixed(1) + "deg)";
      });
      hero.addEventListener("pointerleave", function () {
        stage.style.transform = "";
      });
    }
  }

  /* —— Scroll reveal for feature cards —— */
  if (!reduceMotion && "IntersectionObserver" in window) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    document.querySelectorAll(".ts-feature-card").forEach(function (el, i) {
      el.style.setProperty("--reveal-index", i);
      revealObserver.observe(el);
    });
  } else {
    document.querySelectorAll(".ts-feature-card").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }
})();
