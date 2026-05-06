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

    // Direct-link map: nav items that currently point to redirect stubs
    // are repointed to their final destinations to avoid unnecessary 301
    // hops (SEO audit: "avoid internal redirects").
    var REDIRECT_TARGETS = {
      '/blog-articoli/': '/blog/',
      '/azienda/': '/chi-siamo/',
      '/assistenza/': '/contatti/',
      '/supporto/': '/contatti/',
      '/wiki/': '/contatti/',
      '/wiki-totem-pagamento/': '/contatti/',
      '/wiki-casa-dell-acqua/': '/contatti/',
    };

    var LABELS_TO_REMOVE = new Set([
      'HOME',
      'SUPPORTO',
      'WIKI',
      'WIKI - TOTEM RICARICA',
      "WIKI - CASA DELL'ACQUA",
      "WIKI - CASA DELL\u2019ACQUA",
    ]);

    // 1a. Repoint redirect-targeted links, rename ASSISTENZA, flag items to hide
    document.querySelectorAll('.l-h a[href]').forEach(function (a) {
      var href = a.getAttribute('href') || '';
      var label = (a.textContent || '').trim().toUpperCase();

      // Strip the base prefix to check against REDIRECT_TARGETS
      var relative = href.indexOf(base) === 0 ? href.slice(base.length) : href;
      if (REDIRECT_TARGETS[relative]) {
        a.setAttribute('href', base + REDIRECT_TARGETS[relative]);
      }

      // ASSISTENZA → CONTATTI + strip submenu + no dropdown chevron
      if (label === 'ASSISTENZA') {
        a.textContent = 'CONTATTI';
        a.setAttribute('href', base + '/contatti/');
        var liA = a.closest('li');
        if (liA) {
          liA.classList.remove('wnd-with-submenu');
          liA.querySelectorAll('ul.level-2, ul.level-3, .mm-arrow').forEach(function (el) { el.remove(); });
        }
        return;
      }

      if (LABELS_TO_REMOVE.has(label)) {
        var item = a.closest('li, .menu-item, .nav-item, .sub-menu-item') || a;
        item.classList.add('nav-remove');
      }
    });

    // 1a-bis. AZIENDA top-level: must NOT navigate on click — it's only
    // a submenu opener. Clicking the submenu items goes to their pages
    // (CHI SIAMO → /chi-siamo/ etc.) but the AZIENDA label itself does
    // nothing on click. We target it AFTER the redirect-repoint step
    // so we cleanly remove its href instead of leaving the
    // /chi-siamo/ pointer my redirect rewriter installed.
    document.querySelectorAll('.l-h ul.level-1 > li > .menu-item a, .l-h ul.level-1 > li > a').forEach(function (a) {
      var label = (a.textContent || '').trim().toUpperCase();
      if (label === 'AZIENDA') {
        a.setAttribute('href', '#');
        a.setAttribute('aria-haspopup', 'true');
        a.style.cursor = 'default';
        a.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
        });
      }
    });

    // 1b. Within AZIENDA's submenu, remove the "CONTATTI" entry (CONTATTI
    // is already a top-level item — per client request).
    document.querySelectorAll('.l-h ul.level-1 > li').forEach(function (topLi) {
      var topA = topLi.querySelector(':scope > .menu-item a, :scope > a');
      if (!topA) return;
      var topLabel = (topA.textContent || '').trim().toUpperCase();
      if (topLabel === 'AZIENDA') {
        topLi.querySelectorAll('ul a').forEach(function (subA) {
          if ((subA.textContent || '').trim().toUpperCase() === 'CONTATTI') {
            var subLi = subA.closest('li');
            if (subLi) subLi.classList.add('nav-remove');
          }
        });
      }
    });

    // 1c. After hiding, if a submenu ended up empty, hide the parent too.
    document.querySelectorAll('.l-h ul, .l-h .sub-menu, .l-h .submenu').forEach(function (ul) {
      var visibleChildren = 0;
      ul.querySelectorAll(':scope > li, :scope > .menu-item').forEach(function (li) {
        if (!li.classList.contains('nav-remove')) visibleChildren++;
      });
      if (visibleChildren === 0 && ul !== document.querySelector('.l-h ul')) {
        ul.classList.add('nav-remove');
        var parentLi = ul.closest('li');
        if (parentLi) {
          var parentText = (parentLi.querySelector('a') || {}).textContent;
          if (parentText && /wiki|supporto/i.test(parentText)) {
            parentLi.classList.add('nav-remove');
          }
        }
      }
    });

    // 1d. Reorder top-level menu items: PRODOTTI, SERVIZI, AZIENDA, BLOG, CONTATTI
    var topLevelUl = document.querySelector('.l-h .s-hn ul.level-1');
    if (topLevelUl) {
      var ORDER = ['PRODOTTI', 'SERVIZI', 'AZIENDA', 'BLOG', 'CONTATTI'];
      var topLis = Array.prototype.slice.call(topLevelUl.querySelectorAll(':scope > li'));
      var byLabel = {};
      topLis.forEach(function (li) {
        var a = li.querySelector(':scope > .menu-item a, :scope > a');
        if (!a) return;
        byLabel[(a.textContent || '').trim().toUpperCase()] = li;
      });
      ORDER.forEach(function (lbl) {
        if (byLabel[lbl]) topLevelUl.appendChild(byLabel[lbl]);
      });
    }
  }

  /* ── 2. Transparent-on-home menu ───────────────────────────────── */
  function setupHomeMenu() {
    if (!document.body.classList.contains('is-home')) return;
    var hd = document.querySelector('.l-h');
    if (!hd) return;

    var scrollThreshold = 60;
    function onScroll() {
      if (window.scrollY > scrollThreshold) hd.classList.add('is-scrolled');
      else hd.classList.remove('is-scrolled');
    }

    // Hover detection — any of the following keeps the menu visible:
    //   1. mouse is in the top 140px of the viewport (zone reveal), or
    //   2. mouse is over the .l-h header element OR any of its
    //      descendants (including the level-2 / level-3 dropdowns,
    //      which can extend far below the 140px zone).
    var hoverZoneHeight = 140;
    function onMouseMove(e) {
      var inHeader = e.target && e.target.closest && e.target.closest('.l-h, .l-h *');
      if (e.clientY <= hoverZoneHeight || inHeader) {
        hd.classList.add('is-hovering');
      } else {
        hd.classList.remove('is-hovering');
      }
    }
    document.addEventListener('mousemove', onMouseMove, { passive: true });

    // Direct mouseenter/mouseleave on the header is the most reliable
    // signal when the cursor is anywhere inside it (including dropdowns).
    hd.addEventListener('mouseenter', function () { hd.classList.add('is-hovering'); });
    hd.addEventListener('mouseleave', function () {
      // Only drop is-hovering if mouse also out of the top zone
      hd.classList.remove('is-hovering');
    });

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

    /* ── Viewport sizing ─────────────────────────────────────── */
    /* Slider must always fill the visible viewport BELOW the white
     * social bar (which stays fixed at the top). Measure that bar
     * and feed it into the slider as a CSS custom property so CSS
     * can use calc(100vh - var(--social-bar-h)). */
    function fitSlider() {
      var socialBar = document.querySelector('.l-h .s-hb');
      var h = socialBar ? Math.round(socialBar.getBoundingClientRect().height) : 50;
      wrap.style.setProperty('--social-bar-h', h + 'px');
    }
    fitSlider();
    window.addEventListener('resize', fitSlider, { passive: true });
    // The social bar may render slightly differently after webfonts load
    window.addEventListener('load', fitSlider);

    /* ── Transition rotation ─────────────────────────────────── */
    /* Five distinct effects rotate so consecutive slide changes
     * feel different. Order shuffled so the first transition is
     * the showy "liquid wave". */
    var TRANSITIONS = [
      // 2D effects
      'liquid', 'iris', 'drift', 'glitch', 'zoom',
      // 3D effects
      'flip-card', 'cube', 'fold', 'dive', 'tilt', 'spiral',
    ];
    var transitionIdx = 0;
    var TRANS_DURATION = 1750; // ms — must be >= longest CSS animation (spiral 1.7s)

    var index = 0;
    var timer = null;

    function goTo(i, userTriggered) {
      var n = slideEls.length;
      var target = ((i % n) + n) % n;
      if (target === index && !userTriggered) return;

      var transName = TRANSITIONS[transitionIdx++ % TRANSITIONS.length];

      slideEls.forEach(function (el, j) {
        // Clear every transition class, every state class
        TRANSITIONS.forEach(function (t) { el.classList.remove('is-trans-' + t); });
        el.classList.remove('is-active', 'is-leaving', 'is-entering');

        if (j === target) {
          el.classList.add('is-active', 'is-entering', 'is-trans-' + transName);
        } else if (j === index) {
          el.classList.add('is-leaving', 'is-trans-' + transName);
        }
      });

      // Drop the entering/leaving markers after the animation finishes
      // (CSS sets opacity:1 on .is-active permanently so this is safe).
      window.setTimeout(function () {
        slideEls.forEach(function (el) {
          el.classList.remove('is-entering', 'is-leaving');
          TRANSITIONS.forEach(function (t) { el.classList.remove('is-trans-' + t); });
        });
      }, TRANS_DURATION + 50);

      dots.querySelectorAll('button').forEach(function (b, j) {
        b.classList.toggle('is-active', j === target);
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

  /* ── Auto breadcrumb above H1 ──────────────────────────────────────
   * Build a "PARENT → PAGE" breadcrumb above each page's H1 from the
   * Webnode nav structure: the link with class `wnd-active` is the
   * current page, its first `wnd-with-submenu` ancestor <li> carries
   * the parent label. Both names come straight from the menu, so the
   * breadcrumb stays in sync with whatever the nav shows. Fallback is
   * the page name alone when no parent submenu is found (homepage,
   * top-level pages).
   *
   * Also wipes any pre-existing manual breadcrumbs in the same
   * section: those <h3> blocks containing the U+2192 arrow that some
   * Webnode pages embed before/after the H1 (placement is
   * inconsistent across pages, that's the whole reason for this
   * auto-injection). */
  function injectBreadcrumb() {
    var nav = document.getElementById('menu');
    if (!nav) return;

    /* Standard pages have a `<li class="wnd-active">` for the current
     * page → use the menu label as `current`. Detail pages (blog
     * articles, product/listing details) do NOT have wnd-active
     * because the URL doesn't match any menu item directly → fall
     * back to the deepest `<li class="wnd-active-path">` to anchor
     * the parent lookup, and use the page's H1 text as `current`
     * (the article/detail title is more useful than the submenu
     * label "ARTICOLI DEL BLOG" repeated on every article). */
    var main = document.querySelector('main') || document.body;
    var h1 = main.querySelector('h1');
    if (!h1) return;

    var current = '';
    var activeLi = nav.querySelector('li.wnd-active');
    if (activeLi) {
      var activeText = activeLi.querySelector(':scope > a .menu-item-text');
      if (!activeText) return;
      current = (activeText.textContent || '').trim();
    } else {
      var pathLeafs = nav.querySelectorAll('li.wnd-active-path');
      if (pathLeafs.length > 0) activeLi = pathLeafs[pathLeafs.length - 1];
      current = (h1.textContent || '').trim();
    }
    if (!activeLi || !current) return;

    var parent = '';
    var ancestor = activeLi.parentElement;
    while (ancestor) {
      if (ancestor.tagName === 'LI' && ancestor.classList.contains('wnd-with-submenu')) {
        var pText = ancestor.querySelector(':scope > a .menu-item-text');
        if (pText) {
          parent = (pText.textContent || '').trim();
          break;
        }
      }
      ancestor = ancestor.parentElement;
    }

    var host = h1.parentNode;
    if (host.querySelector(':scope > .artide-breadcrumb')) return;

    var section = h1.closest('section') || main;
    Array.prototype.forEach.call(section.querySelectorAll('h3'), function (h3) {
      if ((h3.textContent || '').indexOf('→') !== -1) h3.remove();
    });

    var bc = document.createElement('div');
    bc.className = 'artide-breadcrumb';
    bc.textContent = parent
      ? parent.toUpperCase() + ' → ' + current.toUpperCase()
      : current.toUpperCase();
    host.insertBefore(bc, h1);
  }

  /* ── Init ──────────────────────────────────────────────────────── */
  function init() {
    try { patchMenu(); } catch (e) { console.warn('[artide] menu patch failed', e); }
    try { setupHomeMenu(); } catch (e) { console.warn('[artide] home menu failed', e); }
    try { mountSlider(); } catch (e) { console.warn('[artide] slider failed', e); }
    try { injectBreadcrumb(); } catch (e) { console.warn('[artide] breadcrumb failed', e); }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
