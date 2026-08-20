/* ============================================================
   GALLERY.JS — Masonry Lightbox Gallery
   ============================================================ */

(function() {
  'use strict';

  // --- Lightbox ---
  class Lightbox {
    constructor() {
      this.overlay = document.getElementById('lightbox');
      this.img     = this.overlay ? this.overlay.querySelector('.lightbox-img') : null;
      this.caption = this.overlay ? this.overlay.querySelector('.lightbox-caption') : null;
      this.closeBtn = this.overlay ? this.overlay.querySelector('.lightbox-close') : null;
      this.items   = [];
      this.current = 0;

      if (!this.overlay) return;
      this.bindEvents();
    }

    open(index) {
      this.current = index || 0;
      const item = this.items[this.current];
      this.img.src = item.src;
      this.img.alt = item.desc || 'Gallery Image';
      
      if(this.caption) {
        if(item.desc) {
          this.caption.innerText = item.desc;
          this.caption.style.display = 'block';
        } else {
          this.caption.style.display = 'none';
        }
      }
      
      this.overlay.classList.add('active');
      document.body.style.overflow = 'hidden';
    }

    close() {
      this.overlay.classList.remove('active');
      document.body.style.overflow = '';
      setTimeout(() => { 
        this.img.src = ''; 
        if(this.caption) this.caption.style.display = 'none';
      }, 400);
    }

    prev() {
      this.current = (this.current - 1 + this.items.length) % this.items.length;
      this.open(this.current);
    }

    next() {
      this.current = (this.current + 1) % this.items.length;
      this.open(this.current);
    }

    bindEvents() {
      this.closeBtn.addEventListener('click', () => this.close());
      this.overlay.addEventListener('click', (e) => {
        if (e.target === this.overlay || e.target === this.caption) this.close();
      });
      document.addEventListener('keydown', (e) => {
        if (!this.overlay.classList.contains('active')) return;
        if (e.key === 'Escape')     this.close();
        if (e.key === 'ArrowLeft')  this.prev();
        if (e.key === 'ArrowRight') this.next();
      });
    }

    register(items) { this.items = items; }
  }

  const lb = new Lightbox();

  // --- LIVE SYNC FROM ADMIN PANEL ---
  const liveSchoolGalleryData = localStorage.getItem('admin_school_gallery');
  if (liveSchoolGalleryData) {
    const grid = document.querySelector('.gallery-grid');
    if (grid) {
      let livePhotos = [];
      try { livePhotos = JSON.parse(liveSchoolGalleryData); } catch(e) {}
      
      // Inject at the beginning of the grid
      livePhotos.reverse().forEach((photo) => {
        const item = document.createElement('div');
        item.className = 'gallery-item';
        item.setAttribute('data-desc', photo.desc || '');
        item.innerHTML = `
          <img src="${photo.image}" alt="${photo.desc || 'School Event'}" loading="lazy" />
          <div class="gallery-overlay"><div class="gallery-zoom-icon"><i class="fa-solid fa-magnifying-glass-plus"></i></div></div>
        `;
        grid.prepend(item);
      });
    }
  }

  // Collect all gallery items and bind them
  const galleryItems = document.querySelectorAll('.gallery-item');
  const itemsData = [];
  
  galleryItems.forEach((item, i) => {
    let src = item.getAttribute('data-src');
    if (!src) {
      const img = item.querySelector('img');
      if (img) src = img.src;
    }
    
    if (src) {
      const desc = item.getAttribute('data-desc') || '';
      itemsData.push({ src, desc });
      item.addEventListener('click', () => lb.open(i));
      item.style.cursor = 'pointer';
    }
  });
  
  lb.register(itemsData);

  window.Lightbox = lb;

})();
