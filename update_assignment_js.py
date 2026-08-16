import os

file_path = r'd:\Gurudev international\Gurudev intenational\js\admin.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_publish = """function publishAssignment() {
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
}"""

new_publish = """function publishAssignment() {
  const classVal = document.getElementById('assign-class').value;
  const subject = document.getElementById('assign-subject').value;
  const title = document.getElementById('assign-title').value;
  const deadline = document.getElementById('assign-deadline').value;
  const fileInput = document.getElementById('assign-file');
  
  if(!classVal || !subject || !title || !deadline) {
    return alert('Please fill all assignment fields.');
  }

  const saveAssignmentData = (fileData = null, fileName = null) => {
    showLoader('Publishing Assignment', 'Notifying Class ' + classVal + '...', 1000, () => {
      let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
      
      assignments.unshift({
        class: classVal,
        subject: subject,
        title: title,
        deadline: deadline,
        dateGiven: new Date().toLocaleDateString('en-GB'),
        fileData: fileData,
        fileName: fileName
      });
      
      try {
        localStorage.setItem('admin_assignments', JSON.stringify(assignments));
        alert('Assignment published successfully!');
      } catch (e) {
        alert('File is too large! Please upload a smaller image.');
        return;
      }
      
      document.getElementById('assign-subject').value = '';
      document.getElementById('assign-title').value = '';
      document.getElementById('assign-deadline').value = '';
      if(fileInput) fileInput.value = '';
      
      loadAdminAssignments();
    });
  };

  if(fileInput && fileInput.files.length > 0) {
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
      saveAssignmentData(e.target.result, file.name);
    };
    reader.readAsDataURL(file);
  } else {
    saveAssignmentData();
  }
}"""

if old_publish in content:
    content = content.replace(old_publish, new_publish)

old_load_assign = """  listBody.innerHTML = '';
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
  });"""

new_load_assign = """  listBody.innerHTML = '';
  assignments.forEach((item, index) => {
    let attachmentHTML = item.fileData ? `<a href="${item.fileData}" target="_blank" style="color:var(--admin-primary); font-size:0.85rem;"><i class="fa-solid fa-paperclip"></i> Attachment</a>` : '';
    listBody.innerHTML += `
      <tr>
        <td>${item.dateGiven}</td>
        <td style="font-weight:600;">Class ${item.class}</td>
        <td>${item.subject}</td>
        <td>
          <div style="font-weight:600;">${item.title}</div>
          ${attachmentHTML}
        </td>
        <td style="color:#ef4444; font-weight:600;">${item.deadline}</td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteAssignment(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });"""

if old_load_assign in content:
    content = content.replace(old_load_assign, new_load_assign)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated js/admin.js successfully.")
