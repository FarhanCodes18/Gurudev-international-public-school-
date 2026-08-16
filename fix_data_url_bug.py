import os

file_path = r'd:\Gurudev international\Gurudev intenational\js\erp-student.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_tt_render = """      myClassTT.forEach(tt => {
        html += `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:16px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
              <span style="font-weight:700; color:#334155;">Class ${tt.class} Timetable</span>
              <span style="font-size:0.85rem; color:#64748b;">Uploaded: ${tt.date}</span>
            </div>
            <a href="${tt.fileData}" target="_blank" class="btn btn-primary" style="display:inline-block; text-decoration:none;"><i class="fa-solid fa-download"></i> View / Download</a>
          </div>
        `;
      });"""

new_tt_render = """      myClassTT.forEach(tt => {
        let isImage = tt.fileData.startsWith('data:image');
        let fileExt = isImage ? 'png' : 'pdf';
        
        let mediaHTML = isImage 
           ? `<div style="margin: 15px 0; border:1px solid #e2e8f0; border-radius:8px; overflow:hidden;"><img src="${tt.fileData}" style="width:100%; display:block;" /></div>`
           : '';
           
        html += `
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:16px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
              <span style="font-weight:700; color:#334155;">Class ${tt.class} Timetable</span>
              <span style="font-size:0.85rem; color:#64748b;">Uploaded: ${tt.date}</span>
            </div>
            ${mediaHTML}
            <a href="${tt.fileData}" download="Class_${tt.class}_Timetable.${fileExt}" class="btn btn-primary" style="display:inline-block; text-decoration:none; width: 100%; text-align: center;"><i class="fa-solid fa-download"></i> Download File</a>
          </div>
        `;
      });"""

if old_tt_render in content:
    content = content.replace(old_tt_render, new_tt_render)

# I should also fix the assignment attachment download just in case!
old_assign_render = """               attachmentHTML = `<div style="margin-top:12px; border-top:1px dashed #cbd5e1; padding-top:12px;"><a href="${a.fileData}" target="_blank" class="btn btn-outline-primary" style="padding:6px 12px; font-size:0.85rem; text-decoration:none; display:inline-block;"><i class="fa-solid fa-download"></i> Download Attachment</a></div>`;"""
new_assign_render = """               attachmentHTML = `<div style="margin-top:12px; border-top:1px dashed #cbd5e1; padding-top:12px;"><a href="${a.fileData}" download="Assignment_Attachment" class="btn btn-outline-primary" style="padding:6px 12px; font-size:0.85rem; text-decoration:none; display:inline-block;"><i class="fa-solid fa-download"></i> Download Attachment</a></div>`;"""

if old_assign_render in content:
    content = content.replace(old_assign_render, new_assign_render)

# Also fix the image preview for assignment to allow downloading instead of opening in _blank which throws a Chromium error
old_assign_img = """               attachmentHTML = `<div style="margin-top:12px; border-top:1px dashed #cbd5e1; padding-top:12px;"><a href="${a.fileData}" target="_blank" style="display:block; border-radius:8px; overflow:hidden; border:1px solid #e2e8f0; max-height:150px;"><img src="${a.fileData}" style="width:100%; object-fit:cover; display:block;" /></a></div>`;"""
new_assign_img = """               attachmentHTML = `<div style="margin-top:12px; border-top:1px dashed #cbd5e1; padding-top:12px;">
                 <a href="${a.fileData}" download="Assignment_Image.png" title="Click to Download" style="display:block; border-radius:8px; overflow:hidden; border:1px solid #e2e8f0; max-height:200px; position:relative;">
                   <img src="${a.fileData}" style="width:100%; object-fit:cover; display:block;" />
                   <div style="position:absolute; bottom:0; left:0; width:100%; background:rgba(0,0,0,0.6); color:white; font-size:0.8rem; padding:6px; text-align:center;"><i class="fa-solid fa-download"></i> Click to Download Image</div>
                 </a>
               </div>`;"""

if old_assign_img in content:
    content = content.replace(old_assign_img, new_assign_img)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed Data URL logic in erp-student.js")
