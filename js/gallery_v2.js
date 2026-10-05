/* ============================================================
   GALLERY.JS — Masonry Lightbox Gallery (No Fallback Data)
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

  // --- LIVE SYNC FROM FIREBASE ---
  const grid = document.querySelector('.gallery-grid');
  if (grid) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#888;">Loading gallery...</div>';
    
    const showEmptyMessage = (isError = false) => {
      grid.innerHTML = `
        <div style="grid-column:1/-1; text-align:center; padding:60px 20px; color:var(--text-muted); font-size:1.1rem;">
          <i class="fa-solid fa-images" style="font-size:3.5rem; margin-bottom:20px; opacity:0.3;"></i><br>
          <span style="font-weight:600; color:var(--text-primary); font-size:1.2rem;">Gallery is currently blank.</span><br>
          <span style="font-size:0.95rem; display:inline-block; margin-top:8px;">Images will appear here once uploaded by the admin.</span>
          ${isError ? '<br><br><span style="font-size:0.8rem; color:#ef4444;">(Database connection failed)</span>' : ''}
        </div>
      `;
    };

    Promise.all([
      import('./firebase-config.js'),
      import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
    ]).then(([config, fs]) => {
      const { collection, getDocs, query, orderBy } = fs;
      getDocs(query(collection(config.db, 'school_gallery'), orderBy('timestamp', 'desc'))).then(snap => {
        
        const renderItems = (photos) => {
          grid.innerHTML = '';
          const itemsData = [];
          let i = 0;
          photos.forEach(photo => {
            const item = document.createElement('div');
            item.className = 'gallery-item';
            item.setAttribute('data-desc', photo.desc || '');
            item.innerHTML = '<img src="'+photo.image+'" alt="'+(photo.desc||'School')+'" loading="lazy" /><div class="gallery-overlay"><div class="gallery-zoom-icon"><i class="fa-solid fa-magnifying-glass-plus"></i></div></div>';
            grid.appendChild(item);
            itemsData.push({ src: photo.image, desc: photo.desc || '' });
            const ci = i; item.addEventListener('click', () => lb.open(ci)); item.style.cursor = 'pointer';
            i++;
          });
          lb.register(itemsData);
        };

        if (snap.empty) { 
          showEmptyMessage(false);
          return; 
        }
        
        const fbPhotos = [];
        snap.forEach(d => fbPhotos.push(d.data()));
        renderItems(fbPhotos);
      }).catch(err => { 
        console.error('Gallery fetch error:', err); 
        showEmptyMessage(true);
      });
    }).catch(err => { 
      console.error('Firebase import error:', err); 
      showEmptyMessage(true);
    });
  }

  window.Lightbox = lb;

})();
