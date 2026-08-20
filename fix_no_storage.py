with open('js/admin.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Firebase Storage upload logic with direct Firestore save
old = """  compressImage(file, 800, 0.6, function(compressedImage) {
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
  });"""

new = """  compressImage(file, 600, 0.5, function(compressedImage) {
    _fbReady.then(fb => {
      if(!fb) { alert('Firebase not ready. Try again.'); if(overlay) overlay.classList.remove('active'); return; }
      const { collection, addDoc } = fb.fs;
      addDoc(collection(fb.db, 'school_gallery'), { image: compressedImage, desc: desc, date: new Date().toLocaleDateString('en-GB'), timestamp: Date.now() }).then(() => {
        alert('Photo uploaded successfully!');
        fileInput.value = ''; if(descInput) descInput.value = '';
        if(document.getElementById('school-gallery-photo-name')) document.getElementById('school-gallery-photo-name').innerText = 'No file chosen';
        if(overlay) overlay.classList.remove('active');
        renderSchoolGalleryList();
      }).catch(err => { console.error('Upload error:', err); alert('Upload failed! Image may be too large.'); if(overlay) overlay.classList.remove('active'); });
    });
  });"""

content = content.replace(old, new)

# Also fix the delete function - remove Storage deletion since we don't use it
old_delete = """function deleteSchoolGallery(id, path) {
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
}"""

new_delete = """function deleteSchoolGallery(id) {
  if(!confirm("Delete this photo?")) return;
  _fbReady.then(fb => {
    if(!fb) return;
    const { doc, deleteDoc } = fb.fs;
    deleteDoc(doc(fb.db, 'school_gallery', id)).then(() => {
      alert('Deleted!'); renderSchoolGalleryList();
    });
  });
}"""

content = content.replace(old_delete, new_delete)

# Fix the render list - remove storagePath from delete button onclick
content = content.replace(
    """onclick="deleteSchoolGallery(\\''+id+'\\',\\''+( item.storagePath||'')+'\\')">\""",
    """onclick="deleteSchoolGallery(\\''+id+'\\')">\""""
)

# Also remove firebase-storage.js from preload since we don't need it
content = content.replace(
    "import('https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js')\n]).then(([c, fs, st]) => ({ db: c.db, storage: c.storage, fs, st })",
    "]).then(([c, fs]) => ({ db: c.db, fs })"
)

with open('js/admin.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated admin.js - No Firebase Storage needed, images saved directly to Firestore")
