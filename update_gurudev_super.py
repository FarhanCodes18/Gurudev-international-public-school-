import os
import re

path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add the sidebar link
nav_link = '<a href="#" class="admin-nav-item" data-target="view-admissions"><i class="fa-solid fa-file-signature"></i> Admissions</a>'
new_nav_link = nav_link + '\n        <a href="#" class="admin-nav-item" data-target="view-registered-students"><i class="fa-solid fa-users"></i> ERP Students</a>'

if 'data-target="view-registered-students"' not in html:
    html = html.replace(nav_link, new_nav_link)

# Add the new section
section_code = """
          <!-- ERP STUDENTS SECTION -->
          <section id="view-registered-students" class="view-section">
            <div class="page-header"><div><h2 class="page-title">Registered ERP Students</h2><p class="page-desc">Live sync with Firebase Database of all ERP portal registrations.</p></div></div>
            <div class="table-container">
              <div class="table-header"><div class="table-title">Student Database</div></div>
              <div class="table-responsive"><table class="admin-table">
                <thead><tr><th>Photo</th><th>Student ID</th><th>Name</th><th>Mobile</th><th>Class</th><th>Gender</th></tr></thead>
                <tbody id="superadmin-students-list">
                  <tr><td colspan="6" style="text-align:center; padding: 30px;">Loading from Firebase...</td></tr>
                </tbody>
              </table></div>
            </div>
          </section>
"""

if 'id="view-registered-students"' not in html:
    html = html.replace('<!-- ADMISSIONS & CALLBACKS -->', section_code + '\n          <!-- ADMISSIONS & CALLBACKS -->')

# Add the Firebase module script at the bottom
firebase_script = """
  <!-- Firebase Logic for Super Admin -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, query, onSnapshot } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

    document.addEventListener('DOMContentLoaded', () => {
      const tbody = document.getElementById('superadmin-students-list');
      if(tbody && db) {
        const q = query(collection(db, 'students'));
        onSnapshot(q, (snapshot) => {
          if (snapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No students registered yet.</td></tr>';
            return;
          }
          tbody.innerHTML = '';
          snapshot.forEach((doc) => {
            const data = doc.data();
            const photo = data.photoURL || 'assets/images/default-avatar.png';
            tbody.innerHTML += `
              <tr>
                <td><img src="${photo}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;"></td>
                <td style="font-weight:600; color:var(--primary);">${data.studentId || 'N/A'}</td>
                <td>${data.name || 'Unknown'}</td>
                <td>${data.mobile || 'N/A'}</td>
                <td>Class ${data.class || '-'}</td>
                <td>${data.gender || '-'}</td>
              </tr>
            `;
          });
        }, (error) => {
          console.error("Firebase read error:", error);
          tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:red;">Failed to connect to Firebase. Check config.</td></tr>';
        });
      }
    });
  </script>
</body>
"""

if 'Firebase Logic for Super Admin' not in html:
    html = html.replace('</body>', firebase_script)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated gurudev-super.html with Firebase integration")
