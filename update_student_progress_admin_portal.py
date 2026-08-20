import os
import re

base_path = r"d:\Gurudev international\Gurudev intenational"
dashboard_html_path = os.path.join(base_path, "erp-dashboard.html")
admin_html_path = os.path.join(base_path, "erp-admin.html")
admin_js_path = os.path.join(base_path, "js", "erp-admin.js")
student_js_path = os.path.join(base_path, "js", "erp-student.js")

# --- 1. Update erp-dashboard.html ---
with open(dashboard_html_path, "r", encoding="utf-8") as f:
    dashboard_content = f.read()

# Lock "Apply Leave"
apply_leave_old = """      <!-- 4 -->
      <div class="feature-card border-pink" style="animation-delay: 0.25s;">
        <div class="icon-box bg-pink-light text-pink"><i class="fa-regular fa-calendar-plus"></i></div>
        <div class="text-box">
          <h3>Apply Leave</h3>
          <p>Submit request</p>
        </div>
      </div>"""
apply_leave_new = """      <!-- 4 -->
      <div class="feature-card locked-card" style="animation-delay: 0.25s;">
        <div class="icon-box bg-gray-light text-gray"><i class="fa-regular fa-calendar-plus"></i></div>
        <div class="text-box">
          <h3>Apply Leave</h3>
          <p class="text-red">Coming Soon</p>
        </div>
        <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
      </div>"""
if apply_leave_old in dashboard_content:
    dashboard_content = dashboard_content.replace(apply_leave_old, apply_leave_new)

# Unlock "My Progress"
my_progress_old = """      <!-- 11 -->
      <div class="feature-card locked-card" style="animation-delay: 0.6s;">
        <div class="icon-box bg-gray-light text-gray"><i class="fa-solid fa-chart-line"></i></div>
        <div class="text-box">
          <h3>My Progress</h3>
          <p class="text-red">Coming Soon</p>
        </div>
        <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
      </div>"""
my_progress_new = """      <!-- 11 -->
      <div class="feature-card border-indigo" onclick="openProgressModal()" style="cursor:pointer; animation-delay: 0.6s;">
        <div class="icon-box bg-indigo-light text-indigo" style="background:#e0e7ff; color:#4f46e5;"><i class="fa-solid fa-chart-line"></i></div>
        <div class="text-box">
          <h3>My Progress</h3>
          <p class="text-indigo">View Performance</p>
        </div>
      </div>"""
if my_progress_old in dashboard_content:
    dashboard_content = dashboard_content.replace(my_progress_old, my_progress_new)

progress_modal_code = """
<!-- Progress Modal -->
<div id="progressModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.7); z-index:9999; justify-content:center; align-items:center; backdrop-filter: blur(4px);">
  <div style="background:#f8fafc; width:95%; max-width:700px; border-radius:20px; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.5); animation: fadeIn 0.3s ease; border: 1px solid rgba(255,255,255,0.2);">
    <div style="padding: 24px; background: linear-gradient(135deg, #4f46e5, #312e81); color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
      <h3 style="margin:0; display:flex; align-items:center; gap:10px; font-size: 1.25rem;"><i class="fa-solid fa-chart-line"></i> My Progress</h3>
      <button onclick="closeProgressModal()" style="background:rgba(255,255,255,0.2); border:none; color:white; width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size:1.2rem; cursor:pointer; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">&times;</button>
    </div>
    <div style="padding: 24px; max-height: 70vh; overflow-y: auto; background: #f8fafc;" id="progressModalBody">
      <div style="text-align:center; padding: 40px; color: #64748b;">
        <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2.5rem; margin-bottom: 15px; color: #4f46e5;"></i>
        <p style="font-weight: 500;">Loading progress from server...</p>
      </div>
    </div>
  </div>
</div>

<script type="module">
  import { db } from './js/firebase-config.js';
  import { collection, query, where, getDocs, orderBy } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

  window.openProgressModal = async function() {
    document.getElementById('progressModal').style.display = 'flex';
    const body = document.getElementById('progressModalBody');
    body.innerHTML = '<div style="text-align:center; padding: 40px; color: #64748b;"><i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2.5rem; margin-bottom: 15px; color: #4f46e5;"></i><p style="font-weight: 500;">Loading progress...</p></div>';
    
    try {
      let user = JSON.parse(localStorage.getItem('erp_current_user'));
      if(!user || !user.studentId) {
        body.innerHTML = '<div style="text-align:center; padding:40px; color:#ef4444;"><i class="fa-solid fa-triangle-exclamation" style="font-size:3rem; margin-bottom:15px;"></i><p>Student profile not found. Please log in again.</p></div>';
        return;
      }

      const progressRef = collection(db, 'student_progress');
      const q = query(progressRef, where('studentId', '==', user.studentId));
      const querySnapshot = await getDocs(q);

      if(querySnapshot.empty) {
        body.innerHTML = '<div style="text-align:center; padding:40px; color:#64748b;"><i class="fa-solid fa-medal" style="font-size: 3rem; color:#cbd5e1; margin-bottom:15px;"></i><p style="font-size:1.1rem;">No progress reports have been uploaded yet.</p></div>';
        return;
      }
      
      // Sort client-side if missing index
      let docsData = [];
      querySnapshot.forEach(doc => {
         docsData.push(doc.data());
      });
      docsData.sort((a, b) => b.timestamp - a.timestamp);
      
      let html = '<div style="display:flex; flex-direction:column; gap:16px;">';
      docsData.forEach(data => {
         const dateObj = data.timestamp ? new Date(data.timestamp) : new Date();
         const dateString = dateObj.toLocaleDateString('en-IN', { year: 'numeric', month: 'long', day: 'numeric' });
         
         html += `
         <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid #4f46e5; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: transform 0.2s ease, box-shadow 0.2s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.05)';">
           <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px dashed #e2e8f0; padding-bottom: 10px;">
             <span style="font-weight: 700; color: #1e293b; font-size: 1.1rem;">Progress Report</span>
             <span style="background: #eef2ff; color: #4f46e5; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;"><i class="fa-regular fa-calendar-days"></i> ${dateString}</span>
           </div>
           <p style="color: #475569; line-height: 1.6; margin: 0;">${data.progressText.replace(/\\n/g, '<br>')}</p>
         </div>`;
      });
      html += '</div>';
      body.innerHTML = html;
      
    } catch(err) {
      console.error(err);
      body.innerHTML = '<div style="text-align:center; padding:40px; color:#ef4444;"><i class="fa-solid fa-triangle-exclamation" style="font-size:3rem; margin-bottom:15px;"></i><p>Failed to load progress. Please check your internet connection.</p></div>';
    }
  }

  window.closeProgressModal = function() {
    document.getElementById('progressModal').style.display = 'none';
  }
</script>
"""

if 'id="progressModal"' not in dashboard_content:
    dashboard_content = dashboard_content.replace('</body>', progress_modal_code + '\n</body>')

with open(dashboard_html_path, "w", encoding="utf-8") as f:
    f.write(dashboard_content)

print("Updated erp-dashboard.html")


# --- 2. Update erp-admin.html ---
with open(admin_html_path, "r", encoding="utf-8") as f:
    admin_content = f.read()

sidebar_new_item = """      <div class="erp-nav-item" data-target="module-progress">
        <i class="fa-solid fa-chart-line"></i> Student Progress
      </div>
      <div class="erp-nav-item" data-target="module-homework">"""
if 'data-target="module-progress"' not in admin_content:
    admin_content = admin_content.replace('      <div class="erp-nav-item" data-target="module-homework">', sidebar_new_item)

progress_module = """      <!-- Module: Student Progress -->
      <div id="module-progress" class="erp-module">
        <div class="erp-card">
          <div class="erp-card-header">
            <div class="erp-card-title">Upload Student Progress</div>
          </div>
          <form style="max-width: 600px;" id="progressForm">
            <div class="form-group">
              <label class="form-label">Select Class</label>
              <select class="form-control" id="progressClassSelect" required>
                <option value="">-- Choose Class --</option>
                <option value="9">Class 9</option>
                <option value="10">Class 10</option>
                <option value="11">Class 11</option>
                <option value="12">Class 12</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Select Student</label>
              <select class="form-control" id="progressStudentSelect" required disabled>
                <option value="">-- Choose Student --</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Progress Report</label>
              <textarea class="form-control" id="progressText" rows="5" required placeholder="Describe the student's progress, achievements, or areas for improvement..."></textarea>
            </div>
            <button type="submit" class="btn btn-primary" id="progressSubmitBtn">Upload Progress</button>
          </form>
        </div>
      </div>
"""

if 'id="module-progress"' not in admin_content:
    admin_content = admin_content.replace('      <div id="module-homework" class="erp-module">', progress_module + '\n      <div id="module-homework" class="erp-module">')

with open(admin_html_path, "w", encoding="utf-8") as f:
    f.write(admin_content)

print("Updated erp-admin.html")


# --- 3. Update js/erp-admin.js ---
with open(admin_js_path, "r", encoding="utf-8") as f:
    admin_js_content = f.read()

# We need to add logic for student progress
progress_js = """
// --- Student Progress Logic ---
import { addDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const progressClassSelect = document.getElementById('progressClassSelect');
const progressStudentSelect = document.getElementById('progressStudentSelect');
const progressForm = document.getElementById('progressForm');
const progressSubmitBtn = document.getElementById('progressSubmitBtn');

if(progressClassSelect && progressStudentSelect) {
  progressClassSelect.addEventListener('change', () => {
    const selectedClass = progressClassSelect.value;
    progressStudentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
    
    if(!selectedClass) {
      progressStudentSelect.disabled = true;
      return;
    }
    
    if(window.allStudentsData && window.allStudentsData.length > 0) {
      const filtered = window.allStudentsData.filter(s => s.class === selectedClass);
      if(filtered.length === 0) {
         progressStudentSelect.innerHTML = '<option value="">No students in this class</option>';
      } else {
         filtered.forEach(student => {
           progressStudentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
         });
         progressStudentSelect.disabled = false;
      }
    } else {
      // Mock mode fallback
      progressStudentSelect.innerHTML += `<option value="GI20261001">Rahul Sharma (GI20261001)</option>`;
      progressStudentSelect.innerHTML += `<option value="GI20261002">Priya Singh (GI20261002)</option>`;
      progressStudentSelect.disabled = false;
    }
  });
}

if(progressForm) {
  progressForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    if(!app) { alert('Mock mode: Progress saved locally.'); return; }
    
    const originalText = progressSubmitBtn.innerHTML;
    progressSubmitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
    progressSubmitBtn.disabled = true;
    
    const studentId = progressStudentSelect.value;
    const studentName = progressStudentSelect.options[progressStudentSelect.selectedIndex].text.split('(')[0].trim();
    const className = progressClassSelect.value;
    const progressText = document.getElementById('progressText').value;
    
    try {
      await addDoc(collection(db, 'student_progress'), {
        studentId: studentId,
        studentName: studentName,
        className: className,
        progressText: progressText,
        timestamp: Date.now(),
        dateStr: new Date().toISOString()
      });
      alert('Progress report successfully uploaded!');
      progressForm.reset();
      progressStudentSelect.disabled = true;
    } catch(err) {
      console.error(err);
      alert('Failed to upload progress.');
    } finally {
      progressSubmitBtn.innerHTML = originalText;
      progressSubmitBtn.disabled = false;
    }
  });
}
"""

if "window.allStudentsData = [];" not in admin_js_content:
    # Need to inject window.allStudentsData population
    admin_js_content = admin_js_content.replace('let total = 0;', 'let total = 0;\n          window.allStudentsData = [];')
    admin_js_content = admin_js_content.replace('querySnapshot.forEach((docSnap) => {', 'querySnapshot.forEach((docSnap) => {\n            window.allStudentsData.push(docSnap.data());')

if "// --- Student Progress Logic ---" not in admin_js_content:
    admin_js_content += "\n" + progress_js

with open(admin_js_path, "w", encoding="utf-8") as f:
    f.write(admin_js_content)

print("Updated erp-admin.js")

# 4. We also need to lock apply leave in js/erp-student.js 
# where it adds a click handler dynamically. Wait, the click handler in js/erp-student.js checks for .locked-card class
# `if(el && !el.classList.contains('locked-card')) { el.addEventListener('click', ...)`
# So we don't need to change js/erp-student.js !

print("Done.")
