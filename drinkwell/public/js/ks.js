/* KrishiSetu — site animations + custom login enhancer */
(function () {
  var LOGIN_IMG = "https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=1400&q=80";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  /* ---------- scroll reveal ---------- */
  function revealSetup() {
    document.body.classList.add("js-ready");
    var sel = ".card,.stat,.chart-card,.scheme,.ks-h2,.ks-lead,.report-hero,.ks-form,.kv,.filterbar,.farmer-card";
    var els = [].slice.call(document.querySelectorAll(sel));
    // stagger items inside a grid
    document.querySelectorAll(".ks-grid").forEach(function (g) {
      [].slice.call(g.children).forEach(function (c, i) {
        c.classList.add("reveal", "d" + Math.min(i % 4 + 1, 4));
      });
    });
    els.forEach(function (e) { if (!e.classList.contains("reveal")) e.classList.add("reveal"); });

    if (!("IntersectionObserver" in window)) {
      document.querySelectorAll(".reveal").forEach(function (e) { e.classList.add("in"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); countUp(en.target); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll(".reveal").forEach(function (e) { io.observe(e); });
  }

  /* ---------- animated counters ---------- */
  function countUp(scope) {
    var ns = scope.matches && scope.matches(".stat,.ks-hero-stats") ? [scope] : [];
    (scope.querySelectorAll ? scope.querySelectorAll(".stat .n, .ks-hero-stats .n") : []).forEach && null;
    var nodes = [];
    if (scope.classList && (scope.classList.contains("stat"))) nodes = [].slice.call(scope.querySelectorAll(".n"));
    nodes.forEach(function (el) {
      var m = /^(\d+(?:\.\d+)?)(%?)$/.exec((el.textContent || "").trim());
      if (!el.dataset.done && m) {
        el.dataset.done = "1";
        var end = parseFloat(m[1]), suf = m[2], dec = m[1].indexOf(".") >= 0 ? 1 : 0, t0 = null, dur = 1100;
        function step(t) {
          if (!t0) t0 = t; var p = Math.min((t - t0) / dur, 1);
          var e = 1 - Math.pow(1 - p, 3);
          el.textContent = (end * e).toFixed(dec) + suf;
          if (p < 1) requestAnimationFrame(step); else el.textContent = m[1] + suf;
        }
        requestAnimationFrame(step);
      }
    });
  }

  /* ---------- nav shrink on scroll ---------- */
  function navScroll() {
    var nav = document.querySelector(".ks-nav");
    if (!nav) return;
    var on = function () { nav.classList.toggle("scrolled", window.scrollY > 24); };
    on(); window.addEventListener("scroll", on, { passive: true });
  }

  /* ---------- custom login ---------- */
  function enhanceLogin() {
    var tries = 0;
    var iv = setInterval(function () {
      tries++;
      var card = document.querySelector(".page-card");
      if (card) {
        clearInterval(iv);
        buildLogin(card);
      } else if (tries > 25) { clearInterval(iv); }
    }, 80);
  }
  function buildLogin(card) {
    document.body.classList.add("ks-login");
    var right = card.parentElement;
    right.classList.add("ks-login-right");
    var split = document.createElement("div");
    split.className = "ks-login-split";
    var left = document.createElement("div");
    left.className = "ks-login-left";
    left.innerHTML =
      '<div class="ks-login-img" style="background-image:url(' + LOGIN_IMG + ')"></div>' +
      '<div class="ks-login-veil"></div>' +
      '<div class="ks-login-content">' +
      '<div class="ks-login-logo"><span class="leaf">🌿</span> KrishiSetu</div>' +
      '<h2>Farmer insights that drive real decisions.</h2>' +
      '<p>Sign in to manage surveys, farmers, schemes and reports across your districts.</p>' +
      '<div class="ks-login-stats"><div><b>396</b><span>Farmers</span></div>' +
      '<div><b>3</b><span>Districts</span></div><div><b>42</b><span>Questions</span></div></div>' +
      '<a href="/" class="ks-login-back">← Back to site</a>' +
      '</div>';
    right.parentNode.insertBefore(split, right);
    split.appendChild(left);
    split.appendChild(right);
    // defensive rebrand of any lingering "Drinkwell" text
    document.querySelectorAll(".page-card-head, .page-card-head *, h4, .text-muted").forEach(function (n) {
      if (n.children.length === 0 && /drinkwell/i.test(n.textContent))
        n.textContent = n.textContent.replace(/drinkwell/ig, "KrishiSetu");
    });
  }

  /* ---------- boot ---------- */
  if (location.pathname.indexOf("/login") === 0) ready(enhanceLogin);
  ready(function () {
    if (document.querySelector(".ks-root")) { revealSetup(); navScroll(); }
  });
})();
