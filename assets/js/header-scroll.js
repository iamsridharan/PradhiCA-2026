/**
 * PradhiCA — sticky nav scroll state (.ec-nav--scrolled)
 */
(function () {
  var nav = document.getElementById("main-nav");
  if (!nav) return;
  function onScroll() {
    nav.classList.toggle("ec-nav--scrolled", window.scrollY > 12);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
})();
