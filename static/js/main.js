/* =====================================================
   FUTOR — Main JavaScript
   Navbar · Dark Mode · Typing · FAQ · Scroll · Forms
   ===================================================== */

document.addEventListener('DOMContentLoaded', function () {

  /* ── 1. PAGE LOADER ─────────────────────────────── */
  const loader = document.getElementById('page-loader');
  if (loader) {
    window.addEventListener('load', () => {
      setTimeout(() => { loader.style.display = 'none'; }, 1300);
    });
  }

  /* ── 2. STICKY NAVBAR + SCROLL-TO-TOP visibility ── */
  const navbar     = document.getElementById('navbar');
  const scrollTopBtn = document.getElementById('scrollTop');

  window.addEventListener('scroll', () => {
    if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 20);
    if (scrollTopBtn) scrollTopBtn.classList.toggle('visible', window.scrollY > 300);
  }, { passive: true });

  /* ── 3. SCROLL TO TOP button ────────────────────── */
  if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── 4. HAMBURGER MENU ──────────────────────────── */
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const open = hamburger.classList.toggle('open');
      navLinks.classList.toggle('open', open);
      hamburger.setAttribute('aria-expanded', open);
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target)) {
        hamburger.classList.remove('open');
        navLinks.classList.remove('open');
      }
    });

    // Close on nav link click (mobile UX)
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        hamburger.classList.remove('open');
        navLinks.classList.remove('open');
      });
    });
  }

  /* ── 5. DARK / LIGHT MODE ───────────────────────── */
  const themeToggle = document.getElementById('themeToggle');
  const themeIcon   = document.getElementById('themeIcon');
  const savedTheme  = localStorage.getItem('futor-theme') || 'light';

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeIcon) {
      themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
  }
  applyTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme');
      const next    = current === 'dark' ? 'light' : 'dark';
      applyTheme(next);
      localStorage.setItem('futor-theme', next);
    });
  }

  /* ── 6. HERO TYPING ANIMATION ───────────────────── */
  const typingEl = document.getElementById('typingText');
  if (typingEl) {
    const word  = 'Futor';
    let   idx   = 0;
    typingEl.textContent = '';

    const timer = setInterval(() => {
      typingEl.textContent += word[idx++];
      if (idx === word.length) {
        clearInterval(timer);
        typingEl.classList.add('done');
      }
    }, 160);
  }

  /* ── 7. FAQ ACCORDION ───────────────────────────── */
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', function () {
      const item   = this.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });

  /* ── 8. AUTO-DISMISS ALERTS (5 s) ──────────────── */
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity    = '0';
      alert.style.transform  = 'translateX(20px)';
      setTimeout(() => alert.remove(), 420);
    }, 5000);
  });

  /* ── 9. SCROLL-REVEAL (cards, sections) ─────────── */
  const revealTargets = document.querySelectorAll(
    '.feature-card, .tutor-card, .why-card, .testimonial-card, ' +
    '.stat-card, .course-step, .subject-chip, .faq-item'
  );

  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity   = '1';
        entry.target.style.transform = 'translateY(0)';
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });

  revealTargets.forEach((el, i) => {
    el.style.opacity    = '0';
    el.style.transform  = 'translateY(24px)';
    el.style.transition = `opacity 0.5s ease ${i * 0.05}s, transform 0.5s ease ${i * 0.05}s`;
    revealObs.observe(el);
  });

  /* ── 10. COUNTER ANIMATION ──────────────────────── */
  function animateCount(el, target, ms) {
    const suffix  = el.dataset.suffix || '';
    const step    = target / (ms / 16);
    let   current = 0;
    const t       = setInterval(() => {
      current += step;
      if (current >= target) {
        el.textContent = target.toLocaleString() + suffix;
        clearInterval(t);
      } else {
        el.textContent = Math.floor(current).toLocaleString() + suffix;
      }
    }, 16);
  }

  const countObs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el  = entry.target;
        const val = parseInt(el.dataset.count);
        if (!isNaN(val)) animateCount(el, val, 1500);
        countObs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('[data-count]').forEach(el => countObs.observe(el));

  /* ── 11. SUBJECT SEARCH SUGGESTIONS ────────────── */
  const SUBJECTS = [
    'Mathematics','Physics','Chemistry','Biology','Science',
    'English','Hindi','Sanskrit','Social Science',
    'Computer Science','Economics','Accountancy'
  ];

  const subjectInput = document.querySelector('input[name="subject"]');
  if (subjectInput) {
    // Create suggestion box
    const box = document.createElement('div');
    box.className = 'search-suggestions';
    Object.assign(box.style, {
      position:'absolute', top:'100%', left:'0', right:'0',
      background:'var(--bg-card)', border:'1.5px solid var(--accent)',
      borderTop:'none', borderRadius:'0 0 8px 8px',
      boxShadow:'var(--shadow)', zIndex:'200', display:'none',
    });
    subjectInput.parentNode.style.position = 'relative';
    subjectInput.parentNode.appendChild(box);

    subjectInput.addEventListener('input', () => {
      const q = subjectInput.value.toLowerCase().trim();
      box.innerHTML = '';
      if (!q) { box.style.display = 'none'; return; }
      const hits = SUBJECTS.filter(s => s.toLowerCase().includes(q));
      if (!hits.length) { box.style.display = 'none'; return; }
      box.style.display = 'block';
      hits.forEach(s => {
        const d = document.createElement('div');
        d.textContent = s;
        Object.assign(d.style, {
          padding:'10px 16px', cursor:'pointer', fontSize:'0.9rem',
          transition:'background 0.15s',
        });
        d.addEventListener('mouseenter', () => d.style.background = 'var(--accent-light)');
        d.addEventListener('mouseleave', () => d.style.background = '');
        d.addEventListener('click', () => {
          subjectInput.value = s;
          box.style.display  = 'none';
        });
        box.appendChild(d);
      });
    });

    document.addEventListener('click', (e) => {
      if (!subjectInput.parentNode.contains(e.target)) box.style.display = 'none';
    });
  }

  /* ── 12. FORM GROUP FOCUS HIGHLIGHT ─────────────── */
  document.querySelectorAll('.form-input, .form-select, .form-textarea').forEach(input => {
    const group = input.closest('.form-group');
    if (!group) return;
    input.addEventListener('focus', () => group.classList.add('focused'));
    input.addEventListener('blur',  () => group.classList.remove('focused'));
  });

  /* ── 13. STAR RATING hover highlight ────────────── */
  const starInputs = document.querySelectorAll('.star-rating input');
  const starLabels = document.querySelectorAll('.star-rating label');

  starLabels.forEach(label => {
    label.addEventListener('mouseenter', function () {
      // star-rating is CSS flex-direction:row-reverse so forloop.counter goes 5→1
      const target = this.getAttribute('for').replace('star', '');
      starLabels.forEach(l => {
        l.style.color = parseInt(l.getAttribute('for').replace('star','')) >= parseInt(target)
          ? '#f59e0b' : '#d1d5db';
      });
    });
    label.addEventListener('mouseleave', () => {
      starLabels.forEach(l => { l.style.color = ''; });
    });
  });

  /* ── 14. ACTIVE NAV LINK by current path ─────────── */
  const path = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    }
  });

  /* ── 15. TABLE ROW HOVER SOUND-FREE feedback ─────── */
  document.querySelectorAll('.data-table tbody tr').forEach(row => {
    row.style.cursor = 'default';
  });

  /* ── 16. IMAGE LAZY LOAD ────────────────────────── */
  if ('IntersectionObserver' in window) {
    const imgObs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imgObs.unobserve(img);
        }
      });
    });
    document.querySelectorAll('img[data-src]').forEach(img => imgObs.observe(img));
  }

});

/* ─── GLOBAL HELPERS (called from templates) ───────── */

/** Toggle a single FAQ item — used via onclick in templates */
function toggleFaq(btn) {
  const item   = btn.closest('.faq-item');
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}

/** Dashboard tab switcher — used via onclick in templates */
function showTab(name) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
  const content = document.getElementById('tab-' + name);
  if (content) content.classList.add('active');
  if (window.event && window.event.target) {
    window.event.target.classList.add('active');
  }
}

/** Password visibility toggle — used in login/register forms */
function togglePass(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon  = document.getElementById(iconId);
  if (!input) return;
  if (input.type === 'password') {
    input.type = 'text';
    if (icon) icon.className = 'fas fa-eye-slash';
  } else {
    input.type = 'password';
    if (icon) icon.className = 'fas fa-eye';
  }
}

/** Alias for single-icon toggle (login page) */
function togglePassword(inputId) {
  togglePass(inputId, 'eyeIcon');
}
