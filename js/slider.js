/* ============================================================
   SLIDER.JS — Hero Image Carousel
   ============================================================ */

(function() {
  'use strict';

  class HeroSlider {
    constructor(container) {
      this.container  = container;
      this.slides     = container.querySelectorAll('.hero-slide');
      this.dots       = container.querySelectorAll('.hero-dot');
      this.prevBtn    = container.querySelector('.hero-arrow.prev');
      this.nextBtn    = container.querySelector('.hero-arrow.next');
      this.current    = 0;
      this.total      = this.slides.length;
      this.interval   = null;
      this.autoDelay  = 5500;
      this.isPlaying  = true;
      this.touchStartX = 0;
      this.touchEndX   = 0;

      if (this.total === 0) return;
      this.init();
    }

    init() {
      this.goTo(0);
      this.startAuto();
      this.bindEvents();
    }

    goTo(index) {
      // Clamp
      this.current = (index + this.total) % this.total;

      // Update slides
      this.slides.forEach((slide, i) => {
        slide.classList.toggle('active', i === this.current);
      });

      // Update dots
      this.dots.forEach((dot, i) => {
        dot.classList.toggle('active', i === this.current);
      });
    }

    next() { this.goTo(this.current + 1); }
    prev() { this.goTo(this.current - 1); }

    startAuto() {
      this.stopAuto();
      this.interval = setInterval(() => this.next(), this.autoDelay);
    }

    stopAuto() {
      if (this.interval) clearInterval(this.interval);
    }

    bindEvents() {
      // Arrow buttons
      if (this.prevBtn) this.prevBtn.addEventListener('click', () => { this.prev(); this.startAuto(); });
      if (this.nextBtn) this.nextBtn.addEventListener('click', () => { this.next(); this.startAuto(); });

      // Dots
      this.dots.forEach((dot, i) => {
        dot.addEventListener('click', () => { this.goTo(i); this.startAuto(); });
      });

      // Touch / swipe
      this.container.addEventListener('touchstart', (e) => {
        this.touchStartX = e.changedTouches[0].clientX;
      }, { passive: true });

      this.container.addEventListener('touchend', (e) => {
        this.touchEndX = e.changedTouches[0].clientX;
        const diff = this.touchStartX - this.touchEndX;
        if (Math.abs(diff) > 50) {
          diff > 0 ? this.next() : this.prev();
          this.startAuto();
        }
      }, { passive: true });

      // Pause on hover
      this.container.addEventListener('mouseenter', () => this.stopAuto());
      this.container.addEventListener('mouseleave', () => this.startAuto());

      // Keyboard
      document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft')  { this.prev(); this.startAuto(); }
        if (e.key === 'ArrowRight') { this.next(); this.startAuto(); }
      });
    }
  }

  // Init all hero sliders
  document.querySelectorAll('.hero-slider').forEach(el => new HeroSlider(el));

  // Expose globally if needed
  window.HeroSlider = HeroSlider;

})();
