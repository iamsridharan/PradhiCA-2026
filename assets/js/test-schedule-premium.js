/**
 * PradhiCA test schedule hub pages — sticky rail, tab sync, 3D tilt, reveal
 */
(function () {
  "use strict";

  var root = document.body;
  if (!root.classList.contains("pg-test-schedule--hub")) return;

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var seriesNav = document.getElementById("ts-series-rail");
  var hero = document.querySelector(".ts-hero");
  var tabLinks = document.querySelectorAll("#ts-series-rail .nav-link[data-toggle='tab']");
  var defaultTab = root.getAttribute("data-ts-default-tab") || "#Tabsabc";

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

  function setActiveSeries(targetId) {
    if (!targetId) return;
    tabLinks.forEach(function (link) {
      var isActive = link.getAttribute("href") === targetId;
      link.classList.toggle("is-current", isActive);
      link.setAttribute("aria-selected", isActive ? "true" : "false");
    });
    document.querySelectorAll(".ts-hero__jump[data-toggle='tab']").forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("href") === targetId);
    });
  }

  tabLinks.forEach(function (link) {
    link.addEventListener("shown.bs.tab", function (e) {
      setActiveSeries(e.target.getAttribute("href"));
    });
  });

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

  if (window.location.hash && document.querySelector(window.location.hash + ".tab-pane")) {
    var hashLink = document.querySelector('#ts-series-rail .nav-link[href="' + window.location.hash + '"]');
    if (hashLink && typeof jQuery !== "undefined") {
      jQuery(hashLink).tab("show");
    }
    setActiveSeries(window.location.hash);
  } else {
    var defaultLink = document.querySelector('#ts-series-rail .nav-link[href="' + defaultTab + '"]');
    if (defaultLink) {
      setActiveSeries(defaultTab);
    } else if (tabLinks.length) {
      setActiveSeries(tabLinks[0].getAttribute("href"));
    }
  }

  if (!reduceMotion) {
    var tiltMax = 8;

    function bindTilt(card) {
      var inner = card.querySelector(".ts-feature-card__inner");
      if (!inner) return;

      card.addEventListener("pointermove", function (e) {
        var rect = card.getBoundingClientRect();
        var x = (e.clientX - rect.left) / rect.width - 0.5;
        var y = (e.clientY - rect.top) / rect.height - 0.5;
        inner.style.transform =
          "rotateX(" + (-y * tiltMax).toFixed(2) + "deg) rotateY(" + (x * tiltMax).toFixed(2) + "deg) translateZ(12px)";
        card.style.setProperty("--spot-x", (x * 50 + 50) + "%");
        card.style.setProperty("--spot-y", (y * 50 + 50) + "%");
      });

      card.addEventListener("pointerleave", function () {
        inner.style.transform = "";
      });
    }

    document.querySelectorAll(".ts-feature-card").forEach(bindTilt);

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
    document.querySelectorAll(".ts-feature-card, .ts-legacy-card").forEach(function (el, i) {
      el.style.setProperty("--reveal-index", i);
      revealObserver.observe(el);
    });
  } else {
    document.querySelectorAll(".ts-feature-card, .ts-legacy-card").forEach(function (el) {
      el.classList.add("is-visible");
    });
  }

  /* DOT 3.0 registration popup (pages with data-ts-dot3-popup) */
  if (root.hasAttribute("data-ts-dot3-popup")) {
    var popup = document.getElementById("ts-dot3-popup");
    var popupKey = "pradhica-foundation-sep26-dot3-popup";
    var popupDelay = 3000;
    var popupTimer = null;
    var lastFocused = null;

    if (popup && !sessionStorage.getItem(popupKey)) {
      function openPopup() {
        lastFocused = document.activeElement;
        popup.removeAttribute("hidden");
        popup.setAttribute("aria-hidden", "false");
        root.classList.add("ts-dot3-popup-open");
        requestAnimationFrame(function () {
          popup.classList.add("is-visible");
        });
        var closeBtn = popup.querySelector(".ts-dot3-popup__close");
        if (closeBtn) closeBtn.focus();
      }

      function closePopup(persist) {
        if (persist) sessionStorage.setItem(popupKey, "1");
        popup.classList.remove("is-visible");
        popup.setAttribute("aria-hidden", "true");
        root.classList.remove("ts-dot3-popup-open");
        window.setTimeout(function () {
          popup.setAttribute("hidden", "");
          if (lastFocused && typeof lastFocused.focus === "function") {
            lastFocused.focus();
          }
        }, 350);
      }

      popupTimer = window.setTimeout(openPopup, popupDelay);

      popup.querySelectorAll("[data-ts-dot3-close]").forEach(function (el) {
        el.addEventListener("click", function () {
          closePopup(true);
        });
      });

      document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && popup.classList.contains("is-visible")) {
          closePopup(true);
        }
      });

      popup.addEventListener("click", function (e) {
        if (e.target === popup.querySelector(".ts-dot3-popup__backdrop")) {
          closePopup(true);
        }
      });
    }
  }
})();
