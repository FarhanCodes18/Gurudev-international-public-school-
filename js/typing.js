/* ============================================================
   TYPING.JS — Typewriter / Cycling Text Effect
   ============================================================ */

(function() {
  'use strict';

  class TypeWriter {
    constructor(element, strings, options = {}) {
      this.el       = element;
      this.strings  = strings;
      this.speed    = options.typeSpeed  || 80;
      this.deleteSpeed = options.deleteSpeed || 50;
      this.pauseEnd = options.pauseEnd   || 2000;
      this.loop     = options.loop !== false;

      this.strIndex = 0;
      this.charIndex = 0;
      this.isDeleting = false;
      this.timer = null;

      // Wrap text in span, add cursor
      this.el.innerHTML = '<span class="type-text"></span><span class="typing-cursor"></span>';
      this.textEl = this.el.querySelector('.type-text');

      this.tick();
    }

    tick() {
      const currentStr = this.strings[this.strIndex % this.strings.length];

      if (this.isDeleting) {
        // Remove a character
        this.textEl.textContent = currentStr.substring(0, this.charIndex - 1);
        this.charIndex--;
      } else {
        // Add a character
        this.textEl.textContent = currentStr.substring(0, this.charIndex + 1);
        this.charIndex++;
      }

      let delay = this.isDeleting ? this.deleteSpeed : this.speed;

      // Finished typing
      if (!this.isDeleting && this.charIndex === currentStr.length) {
        delay = this.pauseEnd;
        this.isDeleting = true;
      }

      // Finished deleting
      if (this.isDeleting && this.charIndex === 0) {
        this.isDeleting = false;
        this.strIndex++;
        delay = 300;
      }

      this.timer = setTimeout(() => this.tick(), delay);
    }

    destroy() {
      if (this.timer) clearTimeout(this.timer);
    }
  }

  // Auto-init on elements with data-typing attribute
  document.querySelectorAll('[data-typing]').forEach(el => {
    try {
      const strings = JSON.parse(el.getAttribute('data-typing'));
      const speed   = parseInt(el.getAttribute('data-type-speed')) || 80;
      const pause   = parseInt(el.getAttribute('data-pause')) || 2000;
      new TypeWriter(el, strings, { typeSpeed: speed, pauseEnd: pause });
    } catch (e) {
      console.warn('TypeWriter init error:', e);
    }
  });

  window.TypeWriter = TypeWriter;

})();
