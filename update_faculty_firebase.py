import sys
import os
import re

def process_super():
    path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'Firebase Faculty Admin Logic' not in content:
        script = '''
  <!-- Firebase Faculty Admin Logic -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, addDoc, deleteDoc, doc, onSnapshot } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

    window.uploadFacultyFirebase = async function() {
      const name = document.getElementById('faculty-name').value.trim();
      const post = document.getElementById('faculty-post').value.trim();
      const spec = document.getElementById('faculty-specialization').value.trim();
      const fileInput = document.getElementById('faculty-photo');

      if (!name || !post) return alert('Please fill Name and Post fields.');
      if (fileInput.files.length === 0) return alert('Please select a photo.');

      const btn = document.querySelector('button[onclick="uploadFaculty()"]');
      const originalText = btn.innerHTML;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
      btn.disabled = true;
      
      compressImage(fileInput.files[0], 600, 0.8, async function(compressedImage) {
        try {
          await addDoc(collection(db, 'faculty'), {
            name: name,
            post: post,
            specialization: spec,
            image: compressedImage,
            timestamp: Date.now()
          });
          alert('Faculty member synced to the Homepage successfully!');
          
          document.getElementById('faculty-name').value = '';
          document.getElementById('faculty-post').value = '';
          document.getElementById('faculty-specialization').value = '';
          fileInput.value = '';
          document.getElementById('faculty-photo-name').innerText = 'No file chosen';
          document.getElementById('faculty-photo-preview').style.display = 'none';
          document.getElementById('faculty-preview-img').style.display = 'none';
          document.getElementById('faculty-preview-placeholder').style.display = 'flex';
          document.getElementById('faculty-preview-name').innerText = 'Faculty Name';
          document.getElementById('faculty-preview-post').innerText = 'Designation';
        } catch(e) {
          console.error(e);
          alert('Error uploading to Firebase.');
        } finally {
          btn.innerHTML = originalText;
          btn.disabled = false;
        }
      });
    };

    // Override the button click
    const uploadBtn = document.querySelector('button[onclick="uploadFaculty()"]');
    if(uploadBtn) {
        uploadBtn.onclick = window.uploadFacultyFirebase;
    }

    window.deleteFacultyFirebase = async function(id) {
      if (!confirm('Are you sure you want to remove this faculty member?')) return;
      try {
        await deleteDoc(doc(db, 'faculty', id));
      } catch(e) {
        console.error(e);
        alert('Failed to delete.');
      }
    };

    // Realtime listener
    onSnapshot(collection(db, 'faculty'), (snapshot) => {
      const tbody = document.getElementById('faculty-list');
      if (!tbody) return;
      
      if (snapshot.empty) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted);">No faculty added yet.</td></tr>';
        return;
      }
      
      let html = '';
      snapshot.forEach(docSnap => {
        const member = docSnap.data();
        html += `
          <tr>
            <td><img src="${member.image}" style="width:50px; height:50px; object-fit:cover; object-position:top; border-radius:50%; border:2px solid var(--admin-border);" alt="${member.name}"></td>
            <td style="font-weight:700; color:var(--admin-heading);">${member.name}</td>
            <td style="color:var(--admin-accent);">${member.post}</td>
            <td style="color:var(--admin-muted);">${member.specialization || '—'}</td>
            <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteFacultyFirebase('${docSnap.id}')"><i class="fa-solid fa-trash"></i></button></td>
          </tr>
        `;
      });
      tbody.innerHTML = html;
    });
  </script>
'''
        content = content.replace('</body>', script + '\n</body>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('gurudev-super.html updated')

def process_index():
    path = r'd:\Gurudev international\Gurudev intenational\index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Firebase Faculty Index Logic' not in content:
        script = '''
  <!-- Firebase Faculty Index Logic -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, onSnapshot, query, orderBy } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

    const wrapper = document.getElementById('faculty-wrapper');
    if (wrapper) {
      const q = query(collection(db, 'faculty'), orderBy('timestamp', 'desc'));
      onSnapshot(q, (snapshot) => {
        let html = '';
        snapshot.forEach(docSnap => {
          const member = docSnap.data();
          html += `
            <div class="swiper-slide">
              <div class="cse-faculty-card" style="transform-style: preserve-3d; transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;"
                onmouseover="this.style.transform='scale(1.08) translateY(-15px) rotateY(10deg)'; this.style.boxShadow='0 25px 50px -12px rgba(0,0,0,0.25)';"
                onmouseout="this.style.transform='scale(1) translateY(0) rotateY(0deg)'; this.style.boxShadow='';">
                <div class="cse-faculty-img">
                  <img src="${member.image}" alt="${member.name}" loading="lazy">
                  <div class="cse-faculty-overlay">
                    <a href="#"><i class="fa-brands fa-linkedin-in"></i></a>
                    <a href="#"><i class="fa-solid fa-envelope"></i></a>
                  </div>
                </div>
                <div class="cse-faculty-info">
                  <h3>${member.name}</h3>
                  <p class="designation">${member.post}</p>
                  <p class="specialization">${member.specialization || 'Faculty'}</p>
                </div>
              </div>
            </div>
          `;
        });
        wrapper.innerHTML = html;
      });
    }
  </script>
'''
        content = content.replace('</body>', script + '\n</body>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('index.html updated')

def process_faculty():
    path = r'd:\Gurudev international\Gurudev intenational\faculty.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # The existing local storage code uses:
    # let faculty = []; try { faculty = JSON.parse(localStorage.getItem('admin_faculty') || '[]'); } catch(e) {}
    # We will replace the entire <script> block for loadAdminFacultyOnFacultyPage
    if 'Firebase Faculty Page Logic' not in content:
        pattern = r'<script>\s*// Dynamically load admin-added faculty into faculty\.html carousel\s*\(function loadAdminFacultyOnFacultyPage\(\) \{[\s\S]*?\}\)\(\);\s*</script>'
        replacement = '''<!-- Firebase Faculty Page Logic -->
<script type="module">
  import { db } from './js/firebase-config.js';
  import { collection, onSnapshot, query, orderBy } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

  const carousel = document.getElementById('facultyCarousel');
  if (carousel) {
    const q = query(collection(db, 'faculty'), orderBy('timestamp', 'asc'));
    onSnapshot(q, (snapshot) => {
      // Remove previously injected firebase cards
      document.querySelectorAll('.firebase-faculty-card').forEach(e => e.remove());
      
      const prevArrow = document.getElementById('facultyPrev');
      
      snapshot.forEach(docSnap => {
        const member = docSnap.data();
        const card = document.createElement('div');
        card.className = 'faculty-card firebase-faculty-card';
        card.setAttribute('data-aos', 'flip-left');
        card.setAttribute('data-aos-duration', '1500');
        card.style.cssText = 'transform-style: preserve-3d; transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;';
        card.setAttribute('onmouseover', 'this.style.transform="scale(1.08) translateY(-15px) rotateY(10deg)"; this.style.boxShadow="0 25px 50px -12px rgba(0,0,0,0.25)";');
        card.setAttribute('onmouseout', 'this.style.transform="scale(1) translateY(0) rotateY(0deg)"; this.style.boxShadow="";');
        card.innerHTML = `
          <div class='faculty-card-img'>
            <img src='${member.image}' alt='${member.name}' loading='lazy' style='object-position:top center;' />
            <div class='faculty-badge'><i class='fa-solid fa-chalkboard-teacher'></i></div>
          </div>
          <div class='faculty-card-body'>
            <h3 class='faculty-name'>${member.name}</h3>
            <div class='faculty-designation'>${member.post}</div>
            <hr class='faculty-divider'>
            <ul class='faculty-details'>
              <li><i class='fa-regular fa-file-lines'></i> ${member.specialization || 'Faculty'}</li>
              <li><i class='fa-solid fa-graduation-cap'></i> Professional</li>
            </ul>
          </div>
        `;
        if (prevArrow) {
          carousel.insertBefore(card, prevArrow);
        } else {
          carousel.appendChild(card);
        }
      });
      
      // Re-trigger the slider initialization logic if possible, 
      // but the inline logic in main_v2.js handles it mostly by DOM checks
      // We will just let main_v2.js do its thing, or if it already cached the cards, it might need updating.
      // But main_v2.js gets querySelectorAll('.faculty-card') at init time.
      // So dynamically adding cards might require us to dispatch an event or reset the faculty track.
      // Actually main_v2 uses facultyTrack.querySelectorAll.
      window.dispatchEvent(new Event('resize'));
    });
  }
</script>'''
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
        else:
            # If pattern not found, just append
            content = content.replace('</body>', replacement + '\n</body>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('faculty.html updated')

if __name__ == '__main__':
    process_super()
    process_index()
    process_faculty()
    print("Done")
