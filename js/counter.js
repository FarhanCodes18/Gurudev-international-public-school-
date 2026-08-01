/* ============================================================
   COUNTER.JS — Animated Number Counter
   ============================================================ */

(function() {
  'use strict';

  function easeOutQuart(t) {
    return 1 - Math.pow(1 - t, 4);
  }

  function animateCounter(el) {
    const target   = parseFloat(el.getAttribute('data-target')) || 0;
    const duration = parseInt(el.getAttribute('data-duration')) || 2000;
    const suffix   = el.getAttribute('data-suffix') || '';
    const prefix   = el.getAttribute('data-prefix') || '';
    const decimals = parseInt(el.getAttribute('data-decimals')) || 0;
    const startTime = performance.now();
    let running = true;

    function update(currentTime) {
      if (!running) return;
      const elapsed  = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased    = easeOutQuart(progress);
      const value    = eased * target;

      el.textContent = prefix + value.toFixed(decimals) + suffix;

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        el.textContent = prefix + target.toFixed(decimals) + suffix;
        el.dispatchEvent(new Event('counter:done'));
      }
    }

    requestAnimationFrame(update);

    return { stop: () => { running = false; } };
  }

  // Use Intersection Observer to trigger counters when visible
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.counted) {
        entry.target.dataset.counted = 'true';
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });

  document.querySelectorAll('[data-counter]').forEach(el => observer.observe(el));

  window.animateCounter = animateCounter;

})();
