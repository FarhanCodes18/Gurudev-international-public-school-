import os

file_path = r'd:\Gurudev international\Gurudev intenational\js\erp-student.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_tt = """  {
    selector: '.feature-card:nth-child(6)',
    title: 'Daily Timetable',
    render: () => emptyState('fa-solid fa-clock-rotate-left', 'Timetable Pending', 'Your class timetable has not been uploaded by the coordinator yet.')
  },"""

new_tt = """  {
    selector: '.feature-card:nth-child(6)',
    title: 'Daily Timetable',
    render: () => {
      let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
      let myClassTT = timetables.filter(t => t.class === user.class);
      
      if(myClassTT.length === 0) {
        return emptyState('fa-solid fa-clock-rotate-left', 'Timetable Pending', 'Your class timetable has not been uploaded by the coordinator yet.');
      }
      
      let html = '<div style="display:flex; flex-direction:column; gap:15px;">';
      myClassTT.forEach(tt => {
        html += `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:16px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
              <span style="font-weight:700; color:#334155;">Class ${tt.class} Timetable</span>
              <span style="font-size:0.85rem; color:#64748b;">Uploaded: ${tt.date}</span>
            </div>
            <a href="${tt.fileData}" target="_blank" class="btn btn-primary" style="display:inline-block; text-decoration:none;"><i class="fa-solid fa-download"></i> View / Download</a>
          </div>
        `;
      });
      html += '</div>';
      return html;
    }
  },"""

if old_tt in content:
    content = content.replace(old_tt, new_tt)

old_assign = """  {
    selector: '.feature-card:nth-child(7)',
    title: 'Assignments',
    render: () => emptyState('fa-solid fa-clipboard-check', 'Hooray! No Homework', 'You have no pending assignments or worksheets to submit.')
  },"""

new_assign = """  {
    selector: '.feature-card:nth-child(7)',
    title: 'Assignments',
    render: () => {
      let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
      let myAssign = assignments.filter(a => a.class === user.class);
      
      if(myAssign.length === 0) {
        return emptyState('fa-solid fa-clipboard-check', 'Hooray! No Homework', 'You have no pending assignments or worksheets to submit.');
      }
      
      let html = '<div style="display:flex; flex-direction:column; gap:15px;">';
      myAssign.forEach(a => {
        html += `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-left:4px solid var(--primary); border-radius:12px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
              <div style="font-weight:700; color:#0f172a; font-size:1.1rem;">${a.title}</div>
              <div style="font-size:0.8rem; background:#fee2e2; color:#ef4444; padding:4px 8px; border-radius:6px; font-weight:700;"><i class="fa-regular fa-clock"></i> Due: ${a.deadline}</div>
            </div>
            <div style="color:#64748b; font-weight:600;"><i class="fa-solid fa-book"></i> Subject: ${a.subject}</div>
            <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">Given on ${a.dateGiven}</div>
          </div>
        `;
      });
      html += '</div>';
      return html;
    }
  },"""

if old_assign in content:
    content = content.replace(old_assign, new_assign)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated js/erp-student.js successfully.")
