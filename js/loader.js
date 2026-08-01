/* ============================================================
   LOADER.JS — Page Preloader
   ============================================================ */

(function() {
  'use strict';

  const loader = document.getElementById('page-loader');
  if (!loader) return;

  // Hide loader when page fully loaded
  window.addEventListener('load', function() {
    setTimeout(function() {
      loader.classList.add('hidden');
      // Remove from DOM after transition
      setTimeout(function() {
        if (loader.parentNode) loader.parentNode.removeChild(loader);
      }, 700);
    }, 800);
  });

  // Fallback: force hide after 4 seconds
  setTimeout(function() {
    loader.classList.add('hidden');
  }, 4000);

})();
