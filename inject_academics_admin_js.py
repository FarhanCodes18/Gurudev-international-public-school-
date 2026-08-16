import os

file_path = r'd:\Gurudev international\Gurudev intenational\js\admin.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

init_calls = """  loadAdminNotices();
  loadAdminLibrary();
  loadAdminResults();
  loadAdminCalendar();
  loadAdminDocuments();
  loadAdminTimetables();
  loadAdminAssignments();
"""

if 'loadAdminTimetables();' not in content:
    content = content.replace("  loadAdminNotices();\n  loadAdminLibrary();\n  loadAdminResults();\n  loadAdminCalendar();\n  loadAdminDocuments();", init_calls.strip())

academics_functions = """

// --- TIMETABLE & ASSIGNMENTS ---
function uploadTimetable() {
  const classVal = document.getElementById('tt-class').value;
  const fileInput = document.getElementById('tt-file');
  
  if(!classVal || fileInput.files.length === 0) {
    return alert('Please select a class and upload a file.');
  }

  const file = fileInput.files[0];
  
  // Basic simulation of upload: converting small files to base64 for localstorage demo
  // In production, upload to Firebase Storage and save URL.
  const reader = new FileReader();
  reader.onload = function(e) {
    let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
    // Remove old timetable for this class if exists
    timetables = timetables.filter(t => t.class !== classVal);
    
    timetables.unshift({
      class: classVal,
      fileData: e.target.result,
      fileName: file.name,
      date: new Date().toLocaleDateString('en-GB')
    });
    
    showLoader('Uploading Timetable', 'Syncing to Student Portal...', 1500, () => {
      try {
        localStorage.setItem('admin_timetables', JSON.stringify(timetables));
        alert('Timetable uploaded successfully!');
        fileInput.value = '';
        loadAdminTimetables();
      } catch(e) {
        alert('File is too large for local storage! Use a smaller file.');
      }
    });
  };
  reader.readAsDataURL(file);
}

function loadAdminTimetables() {
  const listBody = document.getElementById('admin-timetables-list');
  if(!listBody) return;
  
  let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
  
  if(timetables.length === 0) {
    listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No timetables uploaded yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  timetables.forEach((item, index) => {
    listBody.innerHTML += `
      <tr>
        <td>${item.date}</td>
        <td style="font-weight:600;">Class ${item.class}</td>
        <td><a href="${item.fileData}" target="_blank" style="color:var(--admin-primary);"><i class="fa-solid fa-file"></i> ${item.fileName}</a></td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteTimetable(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteTimetable(index) {
  if(!confirm("Are you sure you want to delete this timetable?")) return;
  let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
  timetables.splice(index, 1);
  localStorage.setItem('admin_timetables', JSON.stringify(timetables));
  loadAdminTimetables();
}

function publishAssignment() {
  const classVal = document.getElementById('assign-class').value;
  const subject = document.getElementById('assign-subject').value;
  const title = document.getElementById('assign-title').value;
  const deadline = document.getElementById('assign-deadline').value;
  
  if(!classVal || !subject || !title || !deadline) {
    return alert('Please fill all assignment fields.');
  }
  
  showLoader('Publishing Assignment', 'Notifying Class ' + classVal + '...', 1000, () => {
    let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
    
    assignments.unshift({
      class: classVal,
      subject: subject,
      title: title,
      deadline: deadline,
      dateGiven: new Date().toLocaleDateString('en-GB')
    });
    
    localStorage.setItem('admin_assignments', JSON.stringify(assignments));
    alert('Assignment published successfully!');
    
    document.getElementById('assign-subject').value = '';
    document.getElementById('assign-title').value = '';
    document.getElementById('assign-deadline').value = '';
    
    loadAdminAssignments();
  });
}

function loadAdminAssignments() {
  const listBody = document.getElementById('admin-assignments-list');
  if(!listBody) return;
  
  let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
  
  if(assignments.length === 0) {
    listBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--admin-muted);">No assignments published yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  assignments.forEach((item, index) => {
    listBody.innerHTML += `
      <tr>
        <td>${item.dateGiven}</td>
        <td style="font-weight:600;">Class ${item.class}</td>
        <td>${item.subject}</td>
        <td>${item.title}</td>
        <td style="color:#ef4444; font-weight:600;">${item.deadline}</td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteAssignment(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteAssignment(index) {
  if(!confirm("Are you sure you want to delete this assignment?")) return;
  let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
  assignments.splice(index, 1);
  localStorage.setItem('admin_assignments', JSON.stringify(assignments));
  loadAdminAssignments();
}
"""

if 'function uploadTimetable()' not in content:
    content += academics_functions

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated js/admin.js successfully.")
