import os
import re

file_path = r"d:\Gurudev international\Gurudev intenational\gurudev-super.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Sidebar Link
sidebar_addition = '        <a class="nav-item" data-view="progress"><i class="fa-solid fa-chart-line"></i> Student Progress</a>\n      </div>'
content = content.replace('      </div>\n      \n      <div style="padding: 20px; border-top: 1px solid var(--admin-border);">', sidebar_addition + '\n      \n      <div style="padding: 20px; border-top: 1px solid var(--admin-border);">')


# 2. Add Section
section_html = """
        <!-- STUDENT PROGRESS VIEW -->
        <section id="view-progress" class="view-section">
          <div class="page-header">
            <div><h2 class="page-title">Student Progress</h2><p class="page-desc">Upload performance reports for students.</p></div>
          </div>
          
          <div class="table-container" style="max-width: 700px; padding: 25px;">
            <form id="superProgressForm">
              <div class="form-group" style="margin-bottom: 20px;">
                <label style="display:block; margin-bottom:8px; font-weight:600; color:var(--admin-dark);">Select Class</label>
                <select id="superProgressClassSelect" required style="width:100%; padding:10px 14px; border:1px solid #cbd5e1; border-radius:8px; outline:none;">
                  <option value="">-- Choose Class --</option>
                  <option value="1">Class 1</option>
                  <option value="2">Class 2</option>
                  <option value="3">Class 3</option>
                  <option value="4">Class 4</option>
                  <option value="5">Class 5</option>
                  <option value="6">Class 6</option>
                  <option value="7">Class 7</option>
                  <option value="8">Class 8</option>
                  <option value="9">Class 9</option>
                  <option value="10">Class 10</option>
                  <option value="11">Class 11</option>
                  <option value="12">Class 12</option>
                </select>
              </div>
              
              <div class="form-group" style="margin-bottom: 20px;">
                <label style="display:block; margin-bottom:8px; font-weight:600; color:var(--admin-dark);">Select Student</label>
                <select id="superProgressStudentSelect" required disabled style="width:100%; padding:10px 14px; border:1px solid #cbd5e1; border-radius:8px; outline:none; background:#f8fafc;">
                  <option value="">-- Choose Student --</option>
                </select>
              </div>
              
              <div class="form-group" style="margin-bottom: 20px;">
                <label style="display:block; margin-bottom:8px; font-weight:600; color:var(--admin-dark);">Progress Report</label>
                <textarea id="superProgressText" rows="6" required placeholder="Describe the student's progress, achievements, or areas for improvement..." style="width:100%; padding:14px; border:1px solid #cbd5e1; border-radius:8px; outline:none; resize:vertical; font-family:inherit;"></textarea>
              </div>
              
              <button type="submit" id="superProgressSubmitBtn" class="btn-admin-primary" style="padding:12px 24px; font-size:1rem;"><i class="fa-solid fa-cloud-arrow-up"></i> Upload Progress</button>
            </form>
          </div>
        </section>
"""

# Find where to insert the section. Let's append it right before closing </main>
if '<section id="view-progress"' not in content:
    content = content.replace('      </div>\n    </main>', section_html + '      </div>\n    </main>')


# 3. Add JS Logic for Firebase Upload
js_logic = """
  <!-- Student Progress Logic (Firebase) -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, addDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

    const classSelect = document.getElementById('superProgressClassSelect');
    const studentSelect = document.getElementById('superProgressStudentSelect');
    const progressForm = document.getElementById('superProgressForm');
    const submitBtn = document.getElementById('superProgressSubmitBtn');

    if(classSelect && studentSelect) {
      classSelect.addEventListener('change', () => {
        const selectedClass = classSelect.value;
        studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
        
        if(!selectedClass) {
          studentSelect.disabled = true;
          studentSelect.style.background = '#f8fafc';
          return;
        }
        
        const students = JSON.parse(localStorage.getItem('erp_students')) || [];
        const filtered = students.filter(s => s.class === selectedClass);
        
        if(filtered.length === 0) {
           studentSelect.innerHTML = '<option value="">No students found in this class</option>';
           studentSelect.disabled = true;
           studentSelect.style.background = '#f8fafc';
        } else {
           filtered.forEach(student => {
             studentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
           });
           studentSelect.disabled = false;
           studentSelect.style.background = '#ffffff';
        }
      });
    }

    if(progressForm) {
      progressForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
        submitBtn.disabled = true;
        
        const studentId = studentSelect.value;
        const studentName = studentSelect.options[studentSelect.selectedIndex].text.split('(')[0].trim();
        const className = classSelect.value;
        const progressText = document.getElementById('superProgressText').value;
        
        try {
          await addDoc(collection(db, 'student_progress'), {
            studentId: studentId,
            studentName: studentName,
            className: className,
            progressText: progressText,
            timestamp: Date.now(),
            dateStr: new Date().toISOString()
          });
          
          if(typeof showCustomAlert === 'function') {
             showCustomAlert("Success", "Progress report successfully uploaded to student portal!", "success");
          } else {
             alert('Progress report successfully uploaded to student portal!');
          }
          
          progressForm.reset();
          studentSelect.disabled = true;
          studentSelect.style.background = '#f8fafc';
        } catch(err) {
          console.error("Error uploading progress:", err);
          if(typeof showCustomAlert === 'function') {
             showCustomAlert("Error", "Failed to upload progress. Check console.", "error");
          } else {
             alert('Failed to upload progress.');
          }
        } finally {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }
      });
    }
  </script>
"""

if 'id="superProgressForm"' not in content:
    content = content.replace('</body>', js_logic + '</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added My Progress module to gurudev-super.html successfully.")
