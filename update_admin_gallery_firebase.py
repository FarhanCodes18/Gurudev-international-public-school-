import glob
import re

with open("js/admin.js", "r", encoding="utf-8") as f:
    admin_js = f.read()

firebase_gallery_logic = """// School Gallery Upload & Sync (FIREBASE)
window.uploadSchoolGallery = function() {
  const fileInput = document.getElementById('school-gallery-photo');
  const descInput = document.getElementById('school-gallery-desc');
  
  if(!fileInput || fileInput.files.length === 0) {
    return alert('Please select a photo to upload.');
  }

  const desc = descInput ? descInput.value : '';
  const file = fileInput.files[0];
  
  // Need to show loader but do not auto-close
  const overlay = document.getElementById('admin-loader');
  if(overlay) {
      document.getElementById('loader-title').innerText = 'Uploading Photo';
      document.getElementById('loader-desc').innerText = 'Uploading to cloud database...';
      overlay.classList.add('active');
  }
  
  compressImage(file, 1000, 0.8, function(compressedImage) {
    Promise.all([
      import('./firebase-config.js'),
      import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'),
      import('https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js')
    ]).then(([config, fs, storageFs]) => {
      const db = config.db;
      const storage = config.storage;
      const { collection, addDoc } = fs;
      const { ref, uploadString, getDownloadURL } = storageFs;
      
      const fileName = 'gallery/' + Date.now() + '.jpg';
      const storageRef = ref(storage, fileName);
      
      uploadString(storageRef, compressedImage, 'data_url').then(snapshot => {
        getDownloadURL(snapshot.ref).then(downloadURL => {
          addDoc(collection(db, 'school_gallery'), {
            image: downloadURL,
            desc: desc,
            date: new Date().toLocaleDateString('en-GB'),
            timestamp: Date.now(),
            storagePath: fileName
          }).then(() => {
            alert('Photo uploaded to School Gallery successfully!');
            fileInput.value = '';
            if(descInput) descInput.value = '';
            if(document.getElementById('school-gallery-photo-name')) {
                document.getElementById('school-gallery-photo-name').innerText = 'No file chosen';
            }
            if(overlay) overlay.classList.remove('active');
            renderSchoolGalleryList();
          });
        });
      }).catch(err => {
        console.error("Upload error:", err);
        alert("Upload failed! Check console.");
        if(overlay) overlay.classList.remove('active');
      });
    }).catch(err => {
        console.error("Firebase load error:", err);
        alert("Failed to load Firebase.");
        if(overlay) overlay.classList.remove('active');
    });
  });
}

window.renderSchoolGalleryList = function() {
  const listBody = document.getElementById('school-gallery-list');
  if(!listBody) return;
  
  listBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Loading from cloud...</td></tr>';
  
  Promise.all([
    import('./firebase-config.js'),
    import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
  ]).then(([config, fs]) => {
    const db = config.db;
    const { collection, getDocs, query, orderBy } = fs;
    
    const q = query(collection(db, 'school_gallery'), orderBy('timestamp', 'desc'));
    getDocs(q).then(snapshot => {
      if (snapshot.empty) {
        listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No photos uploaded yet.</td></tr>';
        return;
      }
      
      listBody.innerHTML = '';
      snapshot.forEach(docSnap => {
        const item = docSnap.data();
        const id = docSnap.id;
        listBody.innerHTML += `
          <tr>
            <td><img src="${item.image}" style="width:80px; height:50px; object-fit:cover; border-radius:8px;" alt="Gallery Image"></td>
            <td style="font-weight:600; color:var(--admin-heading);">${item.desc || 'N/A'}</td>
            <td style="color:var(--admin-muted);">${item.date || 'N/A'}</td>
            <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteSchoolGallery('${id}', '${item.storagePath || ''}')"><i class="fa-solid fa-trash"></i></button></td>
          </tr>
        `;
      });
    }).catch(err => {
        listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:red;">Failed to load.</td></tr>';
    });
  });
}

window.deleteSchoolGallery = function(id, storagePath) {
  if(!confirm("Are you sure you want to delete this photo from the cloud?")) return;
  
  const overlay = document.getElementById('admin-loader');
  if(overlay) {
      document.getElementById('loader-title').innerText = 'Deleting Photo';
      document.getElementById('loader-desc').innerText = 'Removing from database and storage...';
      overlay.classList.add('active');
  }
  
  Promise.all([
    import('./firebase-config.js'),
    import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js'),
    import('https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js')
  ]).then(([config, fs, storageFs]) => {
    const db = config.db;
    const storage = config.storage;
    const { doc, deleteDoc } = fs;
    const { ref, deleteObject } = storageFs;
    
    deleteDoc(doc(db, 'school_gallery', id)).then(() => {
      if(storagePath) {
        deleteObject(ref(storage, storagePath)).then(() => {
          alert('Photo deleted successfully!');
          if(overlay) overlay.classList.remove('active');
          renderSchoolGalleryList();
        }).catch(err => {
          console.warn("Storage deletion failed", err);
          alert('Photo deleted successfully!');
          if(overlay) overlay.classList.remove('active');
          renderSchoolGalleryList();
        });
      } else {
        alert('Photo deleted successfully!');
        if(overlay) overlay.classList.remove('active');
        renderSchoolGalleryList();
      }
    });
  });
}"""

admin_js = re.sub(
    r"// School Gallery Upload & Sync.*?function deleteSchoolGallery\(index\) {.*?renderSchoolGalleryList\(\);\n}",
    firebase_gallery_logic,
    admin_js,
    flags=re.DOTALL
)

with open("js/admin.js", "w", encoding="utf-8") as f:
    f.write(admin_js)

print("Updated js/admin.js with Firebase integration for gallery")
