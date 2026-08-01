/* ============================================================
   ANIMATIONS.JS — Intersection Observer Scroll Reveals
   ============================================================ */

(function() {
  'use strict';

  // --- AOS-style data-aos Reveals ---
  const aosObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('aos-animate');
        // Optionally unobserve after first animate
        if (!entry.target.hasAttribute('data-aos-repeat')) {
          aosObserver.unobserve(entry.target);
        }
      } else {
        if (entry.target.hasAttribute('data-aos-repeat')) {
          entry.target.classList.remove('aos-animate');
        }
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

  document.querySelectorAll('[data-aos]').forEach(el => aosObserver.observe(el));

  // --- .reveal class reveals ---
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        // Stagger children if parent has data-stagger
        if (entry.target.hasAttribute('data-stagger')) {
          const children = entry.target.children;
          Array.from(children).forEach((child, i) => {
            child.style.transitionDelay = `${i * 100}ms`;
            child.classList.add('revealed');
          });
          entry.target.classList.add('revealed');
        } else {
          entry.target.classList.add('revealed');
        }
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
    revealObserver.observe(el);
  });

  // --- Timeline Animation ---
  const timelineObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        timelineObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.timeline-item').forEach(el => timelineObserver.observe(el));

  // --- 3D Tilt Effect ---
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', function(e) {
      const rect   = card.getBoundingClientRect();
      const x      = e.clientX - rect.left;
      const y      = e.clientY - rect.top;
      const cx     = rect.width  / 2;
      const cy     = rect.height / 2;
      const rotX   = ((y - cy) / cy) * -8;
      const rotY   = ((x - cx) / cx) * 8;
      card.style.transform = `perspective(1000px) rotateX(${rotX}deg) rotateY(${rotY}deg) scale(1.02)`;
    });

    card.addEventListener('mouseleave', function() {
      card.style.transform = '';
      card.style.transition = 'transform 0.5s ease';
      setTimeout(() => { card.style.transition = ''; }, 500);
    });
  });

  // --- Parallax on scroll ---
  const parallaxEls = document.querySelectorAll('[data-parallax]');

  if (parallaxEls.length > 0) {
    window.addEventListener('scroll', function() {
      const scrollY = window.scrollY;
      parallaxEls.forEach(el => {
        const speed  = parseFloat(el.getAttribute('data-parallax')) || 0.3;
        const rect   = el.getBoundingClientRect();
        const offset = (scrollY - (scrollY + rect.top - window.innerHeight / 2)) * speed;
        el.style.transform = `translateY(${offset}px)`;
      });
    }, { passive: true });
  }

  // --- Stagger children animate ---
  function staggerAnimate(parent, childSelector, baseDelay = 100) {
    const children = parent.querySelectorAll(childSelector);
    children.forEach((child, i) => {
      setTimeout(() => {
        child.classList.add('aos-animate');
      }, i * baseDelay);
    });
  }

  window.staggerAnimate = staggerAnimate;

})();
