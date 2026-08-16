import os

file_path = r'd:\Gurudev international\Gurudev intenational\js\erp-student.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_render = """      myAssign.forEach(a => {
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
      });"""

new_render = """      myAssign.forEach(a => {
        let attachmentHTML = '';
        if(a.fileData) {
            let isImage = a.fileData.startsWith('data:image');
            if(isImage) {
               attachmentHTML = `<div style="margin-top:12px; border-top:1px dashed #cbd5e1; padding-top:12px;"><a href="${a.fileData}" target="_blank" style="display:block; border-radius:8px; overflow:hidden; border:1px solid #e2e8f0; max-height:150px;"><img src="${a.fileData}" style="width:100%; object-fit:cover; display:block;" /></a></div>`;
            } else {
               attachmentHTML = `<div style="margin-top:12px; border-top:1px dashed #cbd5e1; padding-top:12px;"><a href="${a.fileData}" target="_blank" class="btn btn-outline-primary" style="padding:6px 12px; font-size:0.85rem; text-decoration:none; display:inline-block;"><i class="fa-solid fa-download"></i> Download Attachment</a></div>`;
            }
        }
        
        html += `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-left:4px solid var(--primary); border-radius:12px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:8px;">
              <div style="font-weight:700; color:#0f172a; font-size:1.1rem;">${a.title}</div>
              <div style="font-size:0.8rem; background:#fee2e2; color:#ef4444; padding:4px 8px; border-radius:6px; font-weight:700;"><i class="fa-regular fa-clock"></i> Due: ${a.deadline}</div>
            </div>
            <div style="color:#64748b; font-weight:600;"><i class="fa-solid fa-book"></i> Subject: ${a.subject}</div>
            <div style="color:#94a3b8; font-size:0.85rem; margin-top:8px;">Given on ${a.dateGiven}</div>
            ${attachmentHTML}
          </div>
        `;
      });"""

if old_render in content:
    content = content.replace(old_render, new_render)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated js/erp-student.js successfully.")
