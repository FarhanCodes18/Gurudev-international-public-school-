import os

file_path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. gallery-photo
old1 = """<div class="admin-form-group"><label>Upload Photo</label><input type="file" id="gallery-photo" class="admin-input" accept="image/*" /></div>"""
new1 = """<div class="admin-form-group">
  <label>Upload Photo</label>
  <div style="margin-top: 5px;">
    <label class="btn-admin-outline" style="display:inline-block; cursor:pointer; padding: 8px 16px; margin: 0; background: var(--admin-card);">
      <i class="fa-solid fa-cloud-arrow-up"></i> Choose File
      <input type="file" id="gallery-photo" accept="image/*" style="display:none;" onchange="document.getElementById('gallery-photo-name').innerText = this.files[0] ? this.files[0].name : 'No file chosen';" />
    </label>
    <span id="gallery-photo-name" style="margin-left:12px; color:var(--admin-muted); font-size:0.9rem; font-weight: 500;">No file chosen</span>
  </div>
</div>"""

if old1 in content:
    content = content.replace(old1, new1)

# 2. school-gallery-photo
old2 = """<div class="admin-form-group"><label>Upload Photo</label><input type="file" id="school-gallery-photo" class="admin-input" accept="image/*" /></div>"""
new2 = """<div class="admin-form-group">
  <label>Upload Photo</label>
  <div style="margin-top: 5px;">
    <label class="btn-admin-outline" style="display:inline-block; cursor:pointer; padding: 8px 16px; margin: 0; background: var(--admin-card);">
      <i class="fa-solid fa-cloud-arrow-up"></i> Choose File
      <input type="file" id="school-gallery-photo" accept="image/*" style="display:none;" onchange="document.getElementById('school-gallery-photo-name').innerText = this.files[0] ? this.files[0].name : 'No file chosen';" />
    </label>
    <span id="school-gallery-photo-name" style="margin-left:12px; color:var(--admin-muted); font-size:0.9rem; font-weight: 500;">No file chosen</span>
  </div>
</div>"""

if old2 in content:
    content = content.replace(old2, new2)

# 3. news-photo
old3 = """<div class="admin-form-group"><label>Upload Photo</label><input type="file" id="news-photo" class="admin-input" accept="image/*" /></div>"""
new3 = """<div class="admin-form-group">
  <label>Upload Photo</label>
  <div style="margin-top: 5px;">
    <label class="btn-admin-outline" style="display:inline-block; cursor:pointer; padding: 8px 16px; margin: 0; background: var(--admin-card);">
      <i class="fa-solid fa-cloud-arrow-up"></i> Choose File
      <input type="file" id="news-photo" accept="image/*" style="display:none;" onchange="document.getElementById('news-photo-name').innerText = this.files[0] ? this.files[0].name : 'No file chosen';" />
    </label>
    <span id="news-photo-name" style="margin-left:12px; color:var(--admin-muted); font-size:0.9rem; font-weight: 500;">No file chosen</span>
  </div>
</div>"""

if old3 in content:
    content = content.replace(old3, new3)

# 4. bulk-result-file
old4 = """<input type="file" id="bulk-result-file" class="admin-input" accept=".xlsx, .xls, .csv" style="flex:1; margin-bottom:0;" />"""
new4 = """<div style="flex:1; margin-bottom:0; display:flex; align-items:center;">
  <label class="btn-admin-outline" style="display:inline-block; cursor:pointer; padding: 8px 16px; margin: 0; background: var(--admin-card);">
    <i class="fa-solid fa-cloud-arrow-up"></i> Choose File
    <input type="file" id="bulk-result-file" accept=".xlsx, .xls, .csv" style="display:none;" onchange="document.getElementById('bulk-result-file-name').innerText = this.files[0] ? this.files[0].name : 'No file chosen';" />
  </label>
  <span id="bulk-result-file-name" style="margin-left:12px; color:var(--admin-muted); font-size:0.9rem; font-weight: 500;">No file chosen</span>
</div>"""

if old4 in content:
    content = content.replace(old4, new4)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated file inputs in gurudev-super.html successfully.")
