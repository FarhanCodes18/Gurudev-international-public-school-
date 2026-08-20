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

  
  // --- LIVE SYNC FROM FIREBASE ---
  const grid = document.querySelector('.gallery-grid');
  
  if (grid) {
    // Show a loading skeleton or message
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:40px; color:var(--admin-muted);">Loading gallery images...</div>';
    
    // Dynamically import Firebase
    Promise.all([
      import('./js/firebase-config.js'),
      import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
    ]).then(([config, fs]) => {
      const db = config.db;
      const { collection, getDocs, query, orderBy } = fs;
      
      const q = query(collection(db, 'school_gallery'), orderBy('timestamp', 'desc'));
      getDocs(q).then(snapshot => {
        grid.innerHTML = '';
        const itemsData = [];
        
        if (snapshot.empty) {
          grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:40px; color:var(--admin-muted);">No photos uploaded yet.</div>';
          return;
        }

        let i = 0;
        snapshot.forEach(doc => {
          const photo = doc.data();
          const item = document.createElement('div');
          item.className = 'gallery-item';
          item.setAttribute('data-desc', photo.desc || '');
          item.innerHTML = `
            <img src="${photo.image}" alt="${photo.desc || 'School Event'}" loading="lazy" />
            <div class="gallery-overlay"><div class="gallery-zoom-icon"><i class="fa-solid fa-magnifying-glass-plus"></i></div></div>
          `;
          grid.appendChild(item);
          
          itemsData.push({ src: photo.image, desc: photo.desc || '' });
          
          // Bind click event
          const currentIndex = i;
          item.addEventListener('click', () => lb.open(currentIndex));
          item.style.cursor = 'pointer';
          i++;
        });
        
        lb.register(itemsData);
      }).catch(err => {
        console.error("Error fetching gallery:", err);
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:40px; color:red;">Failed to load gallery.</div>';
      });
    }).catch(err => console.error("Firebase import error:", err));
  }

  window.Lightbox = lb;

})();
