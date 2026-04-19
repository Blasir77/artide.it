/*!
 * Artide — Preview override JS
 * - Injects the home hero slider
 * - Patches the navigation (remove HOME, rename Assistenza → Contatti)
 * - Manages transparent-on-home menu with scroll/hover fallback
 */
(function () {
  'use strict';

  /* The base prefix is read from the first <base> tag if present, or from
   * the location pathname so the slider assets resolve correctly both on
   * GitHub Pages and on a future WordPress install. */
  function getBase() {
    var body = document.body;
    if (body && body.dataset && body.dataset.base) return body.dataset.base;
    // Fallback: use the part of the pathname up to /index.html
    var base = '';
    var match = location.pathname.match(/^(.*?)\/(index\.html)?$/);
    if (match && match[1]) base = match[1];
    return base.replace(/\/$/, '');
  }

  /* ── 1. Menu patches ───────────────────────────────────────────── */
  function patchMenu() {
    var base = getBase();
    var links = document.querySelectorAll('.l-h a');
    links.forEach(function (a) {
      var href = a.getAttribute('href') || '';
      var label = (a.textContent || '').trim().toUpperCase();

      // Remove the HOME entry (the literal home link in the nav)
      if (label === 'HOME' && (href === base + '/' || href === '/' || href.endsWith(base + '/'))) {
        // Hide its closest <li> / wrapper, not the <a>
        var item = a.closest('li, .menu-item, .nav-item') || a;
        item.classList.add('nav-remove');
      }

      // Rename ASSISTENZA → CONTATTI and repoint
      if (label === 'ASSISTENZA') {
        a.textContent = 'CONTATTI';
        a.setAttribute('href', base + '/contatti/');
      }
    });
  }

  /* ── 2. Transparent-on-home menu ───────────────────────────────── */
  function setupHomeMenu() {
    if (!document.body.classList.contains('is-home')) return;
    var hd = document.querySelector('.l-h');
    if (!hd) return;
    var threshold = 80;
    function onScroll() {
      if (window.scrollY > threshold) hd.classList.add('is-scrolled');
      else hd.classList.remove('is-scrolled');
    }
    hd.addEventListener('mouseenter', function () { hd.classList.add('is-hovering'); });
    hd.addEventListener('mouseleave', function () { hd.classList.remove('is-hovering'); });
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── 3. Home slider ────────────────────────────────────────────── */

  /* SLIDES is authored here as a plain array so the client can edit
   * images / text / videos for each slide independently.
   * Supported types: 'image', 'video', 'gif' (gif uses <img>). */
  var SLIDES = [
    {
      type: 'image',
      src: '/assets/img/200000086-24c9224c96.webp',
      eyebrow: 'Produttore italiano dal 2003',
      title: "Case dell'Acqua ed erogatori con osmosi inversa",
      subtitle: 'Progettiamo, produciamo e manuteniamo impianti per comuni, aziende e mense. Garanzia a vita.',
      cta: { label: "Scopri le Case dell'Acqua", href: '/casa-dell-acqua/' },
    },
    {
      type: 'image',
      src: '/assets/img/200000093-a9887a988a.webp',
      eyebrow: 'Più di 300 impianti installati',
      title: 'La casa dell’acqua come elemento d’arredo urbano',
      subtitle: 'Oltre 13 modelli — urbani, compatti, a incasso — personalizzabili sul capitolato del tuo Comune.',
      cta: { label: 'Vedi la collezione', href: '/casa-dell-acqua-collezione/' },
    },
    {
      type: 'image',
      src: '/assets/img/200000099-0dd800dd83.webp',
      eyebrow: 'Manutenzione attiva 24/7',
      title: 'Garanzia a vita e telecontrollo in tempo reale',
      subtitle: 'Oltre 500 impianti monitorati H24 dal nostro numero verde con tecnici sempre in sede.',
      cta: { label: 'Servizio manutenzione', href: '/manutenzione/' },
    },
    {
      type: 'image',
      src: '/assets/img/200000107-ed919ed91b.webp',
      eyebrow: 'Erogatori per mense e uffici',
      title: 'Acqua microfiltrata a 0,5 µm direttamente dal tuo rubinetto',
      subtitle: 'Depuratori ad osmosi inversa professionali per condomini, scuole e mense aziendali.',
      cta: { label: 'Vedi erogatori', href: '/erogatore-d-acqua/' },
    },
    {
      type: 'image',
      src: '/assets/img/200000101-34c2434c27.webp',
      eyebrow: 'Riqualificazione impianti',
      title: 'Ridiamo vita alle case dell’acqua di altri produttori',
      subtitle: "Riqualifichiamo, svecchiamo e moderniamo impianti esistenti senza buttare l'infrastruttura.",
      cta: { label: 'Riqualificazione', href: '/trasformazione/' },
    },
  ];

  var SLIDE_DURATION = 15000; // ms between transitions

  function buildSlide(slide, base) {
    var el = document.createElement('div');
    el.className = 'artide-slide';
    var media = document.createElement('div');
    media.className = 'artide-slide-media';
    if (slide.type === 'video') {
      var v = document.createElement('video');
      v.src = base + slide.src;
      v.muted = true; v.loop = true; v.autoplay = true; v.playsInline = true;
      media.appendChild(v);
    } else {
      var img = document.createElement('img');
      img.src = base + slide.src;
      img.alt = slide.title || '';
      img.loading = 'lazy';
      img.decoding = 'async';
      media.appendChild(img);
    }
    el.appendChild(media);
    var content = document.createElement('div');
    content.className = 'artide-slide-content';
    if (slide.eyebrow) {
      var eb = document.createElement('div');
      eb.className = 'artide-slide-eyebrow';
      eb.textContent = slide.eyebrow;
      content.appendChild(eb);
    }
    if (slide.title) {
      var h = document.createElement('h1');
      h.className = 'artide-slide-title';
      h.textContent = slide.title;
      content.appendChild(h);
    }
    if (slide.subtitle) {
      var p = document.createElement('p');
      p.className = 'artide-slide-subtitle';
      p.textContent = slide.subtitle;
      content.appendChild(p);
    }
    if (slide.cta) {
      var a = document.createElement('a');
      a.className = 'artide-slide-cta';
      a.href = base + slide.cta.href;
      a.textContent = slide.cta.label;
      content.appendChild(a);
    }
    el.appendChild(content);
    return el;
  }

  function mountSlider() {
    if (!document.body.classList.contains('is-home')) return;
    var main = document.querySelector('main');
    if (!main) return;
    var wrap = document.createElement('section');
    wrap.id = 'artide-slider';

    var base = getBase();
    var slideEls = SLIDES.map(function (s) { return buildSlide(s, base); });
    slideEls.forEach(function (el) { wrap.appendChild(el); });

    // Dots
    var dots = document.createElement('div');
    dots.className = 'artide-slider-dots';
    SLIDES.forEach(function (_, i) {
      var d = document.createElement('button');
      d.setAttribute('aria-label', 'Vai alla slide ' + (i + 1));
      d.addEventListener('click', function () { goTo(i, true); });
      dots.appendChild(d);
    });
    wrap.appendChild(dots);

    // Arrows
    var prev = document.createElement('button');
    prev.className = 'artide-slider-arrow prev';
    prev.setAttribute('aria-label', 'Slide precedente');
    prev.innerHTML = '‹';
    prev.addEventListener('click', function () { goTo(index - 1, true); });
    var next = document.createElement('button');
    next.className = 'artide-slider-arrow next';
    next.setAttribute('aria-label', 'Slide successiva');
    next.innerHTML = '›';
    next.addEventListener('click', function () { goTo(index + 1, true); });
    wrap.appendChild(prev);
    wrap.appendChild(next);

    main.insertBefore(wrap, main.firstChild);

    var index = 0;
    var timer = null;
    function goTo(i, userTriggered) {
      var n = slideEls.length;
      var target = ((i % n) + n) % n;
      if (target === index && !userTriggered) return;
      slideEls.forEach(function (el, j) {
        el.classList.remove('is-active', 'is-leaving');
        if (j === target) el.classList.add('is-active');
        else if (j === index) el.classList.add('is-leaving');
      });
      dots.querySelectorAll('button').forEach(function (b, j) {
        b.classList.toggle('is-active', j === target);
        // Restart dot animation
        if (j === target) {
          b.style.animation = 'none';
          void b.offsetWidth;
          b.style.animation = '';
        }
      });
      index = target;
      resetTimer();
    }
    function resetTimer() {
      if (timer) clearTimeout(timer);
      timer = setTimeout(function () { goTo(index + 1); }, SLIDE_DURATION);
    }
    goTo(0, true);

    // Pause when tab hidden (saves battery on mobile)
    document.addEventListener('visibilitychange', function () {
      if (document.hidden && timer) { clearTimeout(timer); timer = null; }
      else if (!document.hidden && !timer) { resetTimer(); }
    });
  }

  /* ── Init ──────────────────────────────────────────────────────── */
  function init() {
    try { patchMenu(); } catch (e) { console.warn('[artide] menu patch failed', e); }
    try { setupHomeMenu(); } catch (e) { console.warn('[artide] home menu failed', e); }
    try { mountSlider(); } catch (e) { console.warn('[artide] slider failed', e); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
