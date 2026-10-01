/* =========================================================
   KhedutMitra – Smart Farming Guide
   Main Script
   ========================================================= */

// ---------- Mobile nav toggle ----------
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');

if (navToggle && navLinks) {
  navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });

  // Close menu when a link is clicked
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });
}

// ---------- Crop search (crops.html) ----------
const searchInput = document.getElementById('cropSearch');
const cropsGrid   = document.getElementById('cropsGrid');
const noResults   = document.getElementById('noResults');

if (searchInput && cropsGrid) {
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLowerCase();
    const cards = cropsGrid.querySelectorAll('.searchable');
    let visibleCount = 0;

    cards.forEach(card => {
      const name   = card.dataset.name   || '';
      const season = card.dataset.season || '';
      const soil   = card.dataset.soil   || '';

      const matches = name.includes(query) || season.includes(query) || soil.includes(query);

      card.style.display = matches ? '' : 'none';
      if (matches) visibleCount++;
    });

    if (noResults) {
      noResults.classList.toggle('hidden', visibleCount > 0);
    }
  });
}

// ---------- Scroll-reveal animation ----------
// Add .reveal class to elements we want to animate in
function initReveal() {
  const targets = document.querySelectorAll(
    '.crop-card, .feature-card, .tip-card, .season-card, .detail-card, .stat-card, .advice-item, .plan-tip, .tip-teaser'
  );

  if (!targets.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  targets.forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = `opacity 0.45s ease ${i * 0.06}s, transform 0.45s ease ${i * 0.06}s`;
    observer.observe(el);
  });

  // Add a CSS class that triggers the transition
  document.head.insertAdjacentHTML('beforeend', `
    <style>
      .revealed { opacity: 1 !important; transform: translateY(0) !important; }
    </style>
  `);
}

document.addEventListener('DOMContentLoaded', initReveal);
