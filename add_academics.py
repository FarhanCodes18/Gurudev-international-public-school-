import os

file_path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add link to sidebar
sidebar_link = '<a class="nav-item active" data-view="dashboard"><i class="fa-solid fa-wallet"></i> Fees Portal</a>'
new_sidebar_link = sidebar_link + '\n        <a class="nav-item" data-view="academics"><i class="fa-solid fa-book-open"></i> Timetable & Assignments</a>'
content = content.replace(sidebar_link, new_sidebar_link)

# Add section
section_html = """
        <!-- TIMETABLE & ASSIGNMENTS -->
        <section id="view-academics" class="view-section">
          <div class="page-header"><div><h2 class="page-title">Timetable & Assignments</h2><p class="page-desc">Upload class-wise timetables and homework for students.</p></div></div>
          
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
            <!-- Timetable Upload -->
            <div class="form-card" style="margin-bottom:0;">
              <h3 style="margin-bottom: 15px;">Upload Class Timetable</h3>
              <div class="admin-form-group">
                <label>Select Class</label>
                <select id="tt-class" class="admin-select">
                  <option value="9">Class 9</option>
                  <option value="10">Class 10</option>
                  <option value="11">Class 11</option>
                  <option value="12">Class 12</option>
                </select>
              </div>
              <div class="admin-form-group">
                <label>Upload Timetable (Image/PDF)</label>
                <input type="file" id="tt-file" class="admin-input" accept="image/*,.pdf" />
              </div>
              <button class="btn-admin" onclick="uploadTimetable()"><i class="fa-solid fa-cloud-arrow-up"></i> Sync Timetable</button>
            </div>

            <!-- Assignment Upload -->
            <div class="form-card" style="margin-bottom:0;">
              <h3 style="margin-bottom: 15px;">Publish Assignment / Homework</h3>
              <div class="admin-form-group" style="display:flex; gap:10px;">
                <div style="flex:1;">
                  <label>Class</label>
                  <select id="assign-class" class="admin-select">
                    <option value="9">Class 9</option>
                    <option value="10">Class 10</option>
                    <option value="11">Class 11</option>
                    <option value="12">Class 12</option>
                  </select>
                </div>
                <div style="flex:1;">
                  <label>Subject</label>
                  <input type="text" id="assign-subject" class="admin-input" placeholder="e.g. Maths" />
                </div>
              </div>
              <div class="admin-form-group">
                <label>Assignment Title</label>
                <input type="text" id="assign-title" class="admin-input" placeholder="e.g. Complete Exercise 4.2" />
              </div>
              <div class="admin-form-group">
                <label>Deadline</label>
                <input type="date" id="assign-deadline" class="admin-input" />
              </div>
              <button class="btn-admin" onclick="publishAssignment()"><i class="fa-solid fa-paper-plane"></i> Publish Assignment</button>
            </div>
          </div>

          <div class="table-container" style="margin-top: 30px;">
            <div class="table-header">
              <div class="table-title">Uploaded Timetables</div>
              <button class="btn-admin" style="padding:8px 16px; font-size:0.8rem;" onclick="loadAdminTimetables()"><i class="fa-solid fa-rotate-right"></i> Refresh</button>
            </div>
            <div class="table-responsive"><table class="admin-table">
              <thead><tr><th>Date</th><th>Class</th><th>Timetable File</th><th>Action</th></tr></thead>
              <tbody id="admin-timetables-list">
                <tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No timetables uploaded yet.</td></tr>
              </tbody>
            </table></div>
          </div>

          <div class="table-container" style="margin-top: 30px;">
            <div class="table-header">
              <div class="table-title">Active Assignments</div>
              <button class="btn-admin" style="padding:8px 16px; font-size:0.8rem;" onclick="loadAdminAssignments()"><i class="fa-solid fa-rotate-right"></i> Refresh</button>
            </div>
            <div class="table-responsive"><table class="admin-table">
              <thead><tr><th>Date Given</th><th>Class</th><th>Subject</th><th>Title</th><th>Deadline</th><th>Action</th></tr></thead>
              <tbody id="admin-assignments-list">
                <tr><td colspan="6" style="text-align:center; color:var(--admin-muted);">No assignments published yet.</td></tr>
              </tbody>
            </table></div>
          </div>
        </section>
"""

# Insert section right before ATTENDANCE & STAFF
insert_marker = '<!-- ATTENDANCE & STAFF (Includes Leave Approvals) -->'
if insert_marker in content and 'id="view-academics"' not in content:
    content = content.replace(insert_marker, section_html + '\n        ' + insert_marker)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated gurudev-super.html successfully.")
