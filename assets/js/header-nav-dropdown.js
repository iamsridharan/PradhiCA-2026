/**
 * PradhiCA — reliable Test Series (and other) nav dropdowns on desktop.
 * Fixes hover gap: delayed close + click to toggle.
 */
(function () {
  var DESKTOP = window.matchMedia("(min-width: 992px)");

  function initDesktopDropdowns() {
    var items = document.querySelectorAll(".ec-nav .nav-item__has-dropdown");
    if (!items.length) return;

    items.forEach(function (item) {
      if (item.dataset.dropdownInit === "1") return;
      item.dataset.dropdownInit = "1";

      var toggle = item.querySelector(".dropdown-toggle");
      var closeTimer = null;

      function open() {
        clearTimeout(closeTimer);
        item.classList.add("is-dropdown-open");
        item.classList.add("show");
        if (toggle) toggle.setAttribute("aria-expanded", "true");
      }

      function close(delay) {
        clearTimeout(closeTimer);
        closeTimer = setTimeout(function () {
          item.classList.remove("is-dropdown-open");
          item.classList.remove("show");
          if (toggle) toggle.setAttribute("aria-expanded", "false");
        }, delay == null ? 400 : delay);
      }

      item.addEventListener("mouseenter", open);
      item.addEventListener("mouseleave", function () {
        close(400);
      });

      if (toggle) {
        toggle.addEventListener("click", function (e) {
          if (!DESKTOP.matches) return;
          e.preventDefault();
          e.stopPropagation();
          if (item.classList.contains("is-dropdown-open")) {
            close(0);
          } else {
            open();
          }
        });
      }
    });

    if (!document.body.dataset.dropdownOutsideInit) {
      document.body.dataset.dropdownOutsideInit = "1";
      document.addEventListener("click", function (e) {
        if (!DESKTOP.matches) return;
        if (e.target.closest(".nav-item__has-dropdown")) return;
        document
          .querySelectorAll(".ec-nav .nav-item__has-dropdown.is-dropdown-open")
          .forEach(function (item) {
            item.classList.remove("is-dropdown-open");
            item.classList.remove("show");
            var t = item.querySelector(".dropdown-toggle");
            if (t) t.setAttribute("aria-expanded", "false");
          });
      });
    }
  }

  function boot() {
    if (DESKTOP.matches) initDesktopDropdowns();
  }

  boot();
  DESKTOP.addEventListener("change", boot);
})();
