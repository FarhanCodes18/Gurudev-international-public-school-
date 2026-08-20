import glob
import re

# 1. Update gallery.js
with open("js/gallery.js", "r", encoding="utf-8") as f:
    gallery_js = f.read()

new_sync_logic = """
  // --- LIVE SYNC FROM FIREBASE ---
  const grid = document.querySelector('.gallery-grid');
  
  if (grid) {
    // Show a loading skeleton or message
    grid.innerHTML = '<div style="grid-column: 1/-1; text-align:center; padding:40px; color:var(--admin-muted);">Loading gallery images...</div>';
    
    // Dynamically import Firebase
    Promise.all([
      import('./firebase-config.js'),
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
"""

# Replace the old live sync and binding block
gallery_js = re.sub(
    r"// --- LIVE SYNC FROM ADMIN PANEL ---.*window\.Lightbox = lb;",
    new_sync_logic + "\n  window.Lightbox = lb;",
    gallery_js,
    flags=re.DOTALL
)

with open("js/gallery.js", "w", encoding="utf-8") as f:
    f.write(gallery_js)

print("Updated js/gallery.js")
