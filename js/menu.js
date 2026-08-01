/* ============================================================
   MENU.JS — Mega Menu, Mobile Drawer, Accordion
   ============================================================ */

(function() {
  'use strict';

  // --- Mobile Drawer ---
  const hamburger  = document.querySelector('.hamburger');
  const drawer     = document.querySelector('.mobile-drawer');
  const overlay    = document.querySelector('.mobile-overlay');
  const closeBtn   = document.querySelector('.drawer-close');

  function openDrawer() {
    drawer  && drawer.classList.add('active');
    overlay && overlay.classList.add('active');
    hamburger && hamburger.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    drawer  && drawer.classList.remove('active');
    overlay && overlay.classList.remove('active');
    hamburger && hamburger.classList.remove('active');
    document.body.style.overflow = '';
  }

  hamburger && hamburger.addEventListener('click', () => {
    drawer && drawer.classList.contains('active') ? closeDrawer() : openDrawer();
  });

  overlay  && overlay.addEventListener('click', closeDrawer);
  closeBtn && closeBtn.addEventListener('click', closeDrawer);

  // Close drawer on escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeDrawer();
  });

  // --- Mobile Drawer Accordion (submenu toggle) ---
  document.querySelectorAll('.drawer-nav-link[data-toggle]').forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const submenu = this.nextElementSibling;
      const isOpen  = this.classList.contains('open');

      // Close all
      document.querySelectorAll('.drawer-nav-link.open').forEach(l => {
        l.classList.remove('open');
        const sm = l.nextElementSibling;
        sm && sm.classList.remove('open');
      });

      // Toggle current
      if (!isOpen) {
        this.classList.add('open');
        submenu && submenu.classList.add('open');
      }
    });
  });

  // --- Active nav link highlight ---
  const currentPath = window.location.pathname.split('/').pop();
  document.querySelectorAll('.nav-link, .drawer-nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && href !== '#' && href === currentPath) {
      link.classList.add('active');
    }
  });

  // --- Smooth close drawer on inner link click ---
  drawer && drawer.querySelectorAll('a:not([data-toggle])').forEach(link => {
    link.addEventListener('click', () => {
      setTimeout(closeDrawer, 100);
    });
  });

})();
