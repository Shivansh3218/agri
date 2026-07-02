/* KrishiSetu — site animations + branded login backdrop */
(function () {
  function ready(fn){ if(document.readyState!=="loading") fn(); else document.addEventListener("DOMContentLoaded",fn); }

  /* ---------- scroll reveal ---------- */
  function revealSetup(){
    document.body.classList.add("js-ready");
    var sel=".card,.stat,.chart-card,.scheme,.ks-h2,.ks-lead,.report-hero,.ks-form,.kv,.filterbar,.farmer-card,.kpi";
    document.querySelectorAll(".ks-grid").forEach(function(g){
      [].slice.call(g.children).forEach(function(c,i){ c.classList.add("reveal","d"+Math.min(i%4+1,4)); });
    });
    document.querySelectorAll(sel).forEach(function(e){ if(!e.classList.contains("reveal")) e.classList.add("reveal"); });
    if(!("IntersectionObserver" in window)){ document.querySelectorAll(".reveal").forEach(function(e){e.classList.add("in");}); return; }
    var io=new IntersectionObserver(function(en){ en.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add("in"); countUp(x.target); io.unobserve(x.target);} }); },{threshold:0.12});
    document.querySelectorAll(".reveal").forEach(function(e){ io.observe(e); });
  }
  function countUp(scope){
    if(!(scope.classList&&(scope.classList.contains("stat")||scope.classList.contains("kpi")))) return;
    [].slice.call(scope.querySelectorAll(".n")).forEach(function(el){
      var m=/^(\d+(?:\.\d+)?)(%?)$/.exec((el.textContent||"").trim());
      if(el.dataset.done||!m) return; el.dataset.done="1";
      var end=parseFloat(m[1]),suf=m[2],dec=m[1].indexOf(".")>=0?1:0,t0=null,dur=1000;
      function step(t){ if(!t0)t0=t; var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);
        el.textContent=(end*e).toFixed(dec)+suf; if(p<1)requestAnimationFrame(step); else el.textContent=m[1]+suf; }
      requestAnimationFrame(step);
    });
  }

  /* ---------- nav shrink ---------- */
  function navScroll(){
    var nav=document.querySelector(".ks-nav"); if(!nav) return;
    var on=function(){ nav.classList.toggle("scrolled",window.scrollY>24); };
    on(); window.addEventListener("scroll",on,{passive:true});
  }

  /* ---------- branded login (backdrop only, no form surgery) ---------- */
  function enhanceLogin(){
    var tries=0, iv=setInterval(function(){
      tries++;
      var card=document.querySelector(".page-card");
      if(card){ clearInterval(iv); paintLogin(); }
      else if(tries>30) clearInterval(iv);
    },80);
  }
  function paintLogin(){
    document.body.classList.add("ks-login");
    if(!document.querySelector(".ks-login-brand")){
      var b=document.createElement("div"); b.className="ks-login-brand";
      b.innerHTML='<div class="lg"><span class="leaf">&#127807;</span> KrishiSetu</div>'+
        '<p>Farmer insights that drive real decisions</p>';
      document.body.appendChild(b);
    }
    if(!document.querySelector(".ks-login-back")){
      var a=document.createElement("a"); a.className="ks-login-back"; a.href="/"; a.innerHTML="&larr; Back to site";
      document.body.appendChild(a);
    }
    // rebrand any lingering "Drinkwell" text
    document.querySelectorAll(".page-card-head, .page-card-head *").forEach(function(n){
      if(n.children.length===0 && /drinkwell/i.test(n.textContent))
        n.textContent=n.textContent.replace(/drinkwell/ig,"KrishiSetu");
    });
  }

  if(location.pathname.indexOf("/login")===0) ready(enhanceLogin);
  ready(function(){ if(document.querySelector(".ks-root")){ revealSetup(); navScroll(); } });
})();
