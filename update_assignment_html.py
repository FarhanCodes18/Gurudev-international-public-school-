import os

file_path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_html = """              <div class="admin-form-group">
                <label>Deadline</label>
                <input type="date" id="assign-deadline" class="admin-input" />
              </div>
              <button class="btn-admin" onclick="publishAssignment()"><i class="fa-solid fa-paper-plane"></i> Publish Assignment</button>"""

new_html = """              <div class="admin-form-group">
                <label>Deadline</label>
                <input type="date" id="assign-deadline" class="admin-input" />
              </div>
              <div class="admin-form-group">
                <label>Upload Image/File (Optional)</label>
                <input type="file" id="assign-file" class="admin-input" accept="image/*,.pdf" />
              </div>
              <button class="btn-admin" onclick="publishAssignment()"><i class="fa-solid fa-paper-plane"></i> Publish Assignment</button>"""

if old_html in content:
    content = content.replace(old_html, new_html)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated gurudev-super.html successfully.")
