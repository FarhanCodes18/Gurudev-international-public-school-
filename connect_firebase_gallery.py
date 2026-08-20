import re

# =============================================
# 1. UPDATE js/admin.js — Firebase gallery upload, render, delete
# =============================================
with open('js/admin.js', 'r', encoding='utf-8') as f:
    admin = f.read()

# Add Firebase preload at the very top
admin = admin.replace(
    '/* admin.js - Superpower Admin Panel Logic (Light Theme & Sync Updates) */',
    '''/* admin.js - Superpower Admin Panel Logic (Light Theme & Sync Updates) */
// Preload Firebase SDKs so uploads are instant
var _fbReady = Promise.all([
  import('./js/firebase-config.js'),
  import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'),
  import('https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js')
]).then(([c, fs, st]) => ({ db: c.db, storage: c.storage, fs, st })).catch(e => { console.warn('Firebase preload:', e); return null; });'''
)

# Replace uploadSchoolGallery
old_upload = '''// School Gallery Upload & Sync
function uploadSchoolGallery() {
  const fileInput = document.getElementById('school-gallery-photo');
  const descInput = document.getElementById('school-gallery-desc');
  
  if(fileInput.files.length === 0) {
    return alert('Please select a photo to upload.');
  }

  const desc = descInput ? descInput.value : '';
  const file = fileInput.files[0];
  
  compressImage(file, 800, 0.7, function(compressedImage) {
    let gallery = JSON.parse(localStorage.getItem('admin_school_gallery') || '[]');
    
    gallery.unshift({ image: compressedImage, desc: desc, date: new Date().toLocaleDateString() });
    
    showLoader('Uploading Photo', 'Optimizing and syncing to the School Gallery...', 2000, () => {
      try {
        localStorage.setItem('admin_school_gallery', JSON.stringify(gallery));
        alert('Photo synced to the School Gallery successfully!');
      } catch(e) {
        alert('Storage full! Delete some old photos first.');
      }
      fileInput.value = '';
      if(descInput) descInput.value = '';
      renderSchoolGalleryList();
    });
  });
}'''

new_upload = '''// School Gallery Upload & Sync (FIREBASE)
function uploadSchoolGallery() {
  const fileInput = document.getElementById('school-gallery-photo');
  const descInput = document.getElementById('school-gallery-desc');
  if(!fileInput || fileInput.files.length === 0) return alert('Please select a photo to upload.');
  const desc = descInput ? descInput.value : '';
  const file = fileInput.files[0];
  const overlay = document.getElementById('admin-loader');
  if(overlay) { document.getElementById('loader-title').innerText = 'Uploading Photo'; document.getElementById('loader-desc').innerText = 'Uploading to cloud...'; overlay.classList.add('active'); }
  compressImage(file, 800, 0.6, function(compressedImage) {
    _fbReady.then(fb => {
      if(!fb) { alert('Firebase not ready. Try again.'); if(overlay) overlay.classList.remove('active'); return; }
      const { ref, uploadString, getDownloadURL } = fb.st;
      const { collection, addDoc } = fb.fs;
      const fileName = 'gallery/' + Date.now() + '.jpg';
      const storageRef = ref(fb.storage, fileName);
      uploadString(storageRef, compressedImage, 'data_url').then(snap => {
        getDownloadURL(snap.ref).then(url => {
          addDoc(collection(fb.db, 'school_gallery'), { image: url, desc: desc, date: new Date().toLocaleDateString('en-GB'), timestamp: Date.now(), storagePath: fileName }).then(() => {
            alert('Photo uploaded successfully!');
            fileInput.value = ''; if(descInput) descInput.value = '';
            if(document.getElementById('school-gallery-photo-name')) document.getElementById('school-gallery-photo-name').innerText = 'No file chosen';
            if(overlay) overlay.classList.remove('active');
            renderSchoolGalleryList();
          });
        });
      }).catch(err => { console.error('Upload error:', err); alert('Upload failed!'); if(overlay) overlay.classList.remove('active'); });
    });
  });
}'''

admin = admin.replace(old_upload, new_upload)

# Replace renderSchoolGalleryList
old_render = '''// Render School Gallery List
function renderSchoolGalleryList() {
  const listBody = document.getElementById('school-gallery-list');
  if(!listBody) return;
  
  let gallery = JSON.parse(localStorage.getItem('admin_school_gallery') || '[]');
  
  if(gallery.length === 0) {
    listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No photos uploaded yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  gallery.forEach((item, index) => {
    listBody.innerHTML += `
      <tr>
        <td><img src="${item.image}" style="width:80px; height:50px; object-fit:cover; border-radius:8px;" alt="Gallery Image"></td>
        <td style="font-weight:600; color:var(--admin-heading);">${item.desc || 'N/A'}</td>
        <td style="color:var(--admin-muted);">${item.date || 'N/A'}</td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteSchoolGallery(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteSchoolGallery(index) {
  if(!confirm("Are you sure you want to delete this photo?")) return;
  let gallery = JSON.parse(localStorage.getItem('admin_school_gallery') || '[]');
  gallery.splice(index, 1);
  localStorage.setItem('admin_school_gallery', JSON.stringify(gallery));
  renderSchoolGalleryList();
}'''

new_render = '''// Render School Gallery List (FIREBASE)
function renderSchoolGalleryList() {
  const listBody = document.getElementById('school-gallery-list');
  if(!listBody) return;
  listBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Loading...</td></tr>';
  _fbReady.then(fb => {
    if(!fb) { listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:red;">Firebase not connected.</td></tr>'; return; }
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'school_gallery'), orderBy('timestamp', 'desc'))).then(snap => {
      if(snap.empty) { listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No photos uploaded yet.</td></tr>'; return; }
      listBody.innerHTML = '';
      snap.forEach(d => {
        const item = d.data(); const id = d.id;
        listBody.innerHTML += '<tr><td><img src="'+item.image+'" style="width:80px;height:50px;object-fit:cover;border-radius:8px;" alt="Gallery"></td><td style="font-weight:600;color:var(--admin-heading);">'+(item.desc||'N/A')+'</td><td style="color:var(--admin-muted);">'+(item.date||'N/A')+'</td><td><button class="btn-admin" style="background:#ef4444;padding:6px 12px;font-size:0.8rem;" onclick="deleteSchoolGallery(\''+id+'\',\''+( item.storagePath||'')+'\')"><i class="fa-solid fa-trash"></i></button></td></tr>';
      });
    });
  });
}

function deleteSchoolGallery(id, path) {
  if(!confirm("Delete this photo?")) return;
  _fbReady.then(fb => {
    if(!fb) return;
    const { doc, deleteDoc } = fb.fs;
    const { ref, deleteObject } = fb.st;
    deleteDoc(doc(fb.db, 'school_gallery', id)).then(() => {
      if(path) deleteObject(ref(fb.storage, path)).catch(()=>{});
      alert('Deleted!'); renderSchoolGalleryList();
    });
  });
}'''

admin = admin.replace(old_render, new_render)

with open('js/admin.js', 'w', encoding='utf-8') as f:
    f.write(admin)
print("1. Updated js/admin.js with Firebase gallery")

# =============================================
# 2. UPDATE js/gallery.js — Read from Firebase
# =============================================
with open('js/gallery.js', 'r', encoding='utf-8') as f:
    gallery = f.read()

old_sync = '''  // --- LIVE SYNC FROM ADMIN PANEL ---
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

  window.Lightbox = lb;'''

new_sync = '''  // --- LIVE SYNC FROM FIREBASE ---
  const grid = document.querySelector('.gallery-grid');
  if (grid) {
    grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#888;">Loading gallery...</div>';
    Promise.all([
      import('./js/firebase-config.js'),
      import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
    ]).then(([config, fs]) => {
      const { collection, getDocs, query, orderBy } = fs;
      getDocs(query(collection(config.db, 'school_gallery'), orderBy('timestamp', 'desc'))).then(snap => {
        grid.innerHTML = '';
        const itemsData = [];
        if (snap.empty) { grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:#888;">No photos uploaded yet. Upload from Admin Panel.</div>'; return; }
        let i = 0;
        snap.forEach(d => {
          const photo = d.data();
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
      }).catch(err => { console.error('Gallery fetch error:', err); grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:red;">Failed to load gallery.</div>'; });
    }).catch(err => { console.error('Firebase import error:', err); grid.innerHTML = '<div style="grid-column:1/-1;text-align:center;padding:40px;color:red;">Failed to connect.</div>'; });
  }

  window.Lightbox = lb;'''

gallery = gallery.replace(old_sync, new_sync)

with open('js/gallery.js', 'w', encoding='utf-8') as f:
    f.write(gallery)
print("2. Updated js/gallery.js with Firebase read")

# =============================================
# 3. REMOVE fake photos from gallery.html
# =============================================
with open('gallery.html', 'r', encoding='utf-8') as f:
    ghtml = f.read()

# Remove everything between gallery-grid open and close, replace with empty + comment
import re
ghtml = re.sub(
    r"(<div class='gallery-grid' id='main-gallery-grid'>)\s*\n.*?(\n</div>\n</div></section>)",
    r"\1\n    <!-- Photos loaded from Firebase -->\n</div>\n</div></section>",
    ghtml,
    flags=re.DOTALL
)

with open('gallery.html', 'w', encoding='utf-8') as f:
    f.write(ghtml)
print("3. Removed fake photos from gallery.html")

# =============================================
# 4. REMOVE fake photos from index.html gallery section
# =============================================
with open('index.html', 'r', encoding='utf-8') as f:
    ihtml = f.read()

ihtml = re.sub(
    r'(<div class="gallery-grid">)\s*\n.*?(\n      </div>\n    </div>\n  </section>)',
    r'\1\n        <!-- Photos loaded from Firebase -->\n      </div>\n    </div>\n  </section>',
    ihtml,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(ihtml)
print("4. Removed fake photos from index.html")

# =============================================
# 5. Bump cache version on gurudev-super.html
# =============================================
with open('gurudev-super.html', 'r', encoding='utf-8') as f:
    superhtml = f.read()

superhtml = superhtml.replace('js/admin.js?v=3', 'js/admin.js?v=4')

with open('gurudev-super.html', 'w', encoding='utf-8') as f:
    f.write(superhtml)
print("5. Bumped admin.js cache to v=4")

print("\nAll done! Firebase gallery is now connected.")
