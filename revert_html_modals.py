import os

file_path = r'd:\Gurudev international\Gurudev intenational\erp-dashboard.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Revert inline onclicks
content = content.replace(' onclick="openTimetableModal()" style="cursor:pointer;"', '')
content = content.replace(' onclick="openAssignmentsModal()" style="cursor:pointer;"', '')

# Remove injected modals
modals = """
<!-- Timetable Modal -->
<div id="timetableModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.7); z-index:9999; justify-content:center; align-items:center; backdrop-filter: blur(4px);">
  <div style="background:#f8fafc; width:95%; max-width:800px; border-radius:20px; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.2);">
    <div style="padding: 24px; background: linear-gradient(135deg, #ef4444, #b91c1c); color: white; display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin:0; display:flex; align-items:center; gap:10px; font-size: 1.25rem;"><i class="fa-regular fa-clock"></i> Class Timetable</h3>
      <button onclick="document.getElementById('timetableModal').style.display='none'" style="background:rgba(255,255,255,0.2); border:none; color:white; width: 32px; height: 32px; border-radius: 50%; font-size:1.2rem; cursor:pointer;">&times;</button>
    </div>
    <div style="padding: 24px; max-height: 70vh; overflow-y: auto;" id="timetableModalBody">
      <div style="text-align:center; padding: 40px; color: #64748b;">Loading timetable...</div>
    </div>
  </div>
</div>

<!-- Assignments Modal -->
<div id="assignmentsModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.7); z-index:9999; justify-content:center; align-items:center; backdrop-filter: blur(4px);">
  <div style="background:#f8fafc; width:95%; max-width:800px; border-radius:20px; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.2);">
    <div style="padding: 24px; background: linear-gradient(135deg, #14b8a6, #0f766e); color: white; display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin:0; display:flex; align-items:center; gap:10px; font-size: 1.25rem;"><i class="fa-solid fa-book-open"></i> Pending Assignments</h3>
      <button onclick="document.getElementById('assignmentsModal').style.display='none'" style="background:rgba(255,255,255,0.2); border:none; color:white; width: 32px; height: 32px; border-radius: 50%; font-size:1.2rem; cursor:pointer;">&times;</button>
    </div>
    <div style="padding: 24px; max-height: 70vh; overflow-y: auto;" id="assignmentsModalBody">
      <div style="text-align:center; padding: 40px; color: #64748b;">Loading assignments...</div>
    </div>
  </div>
</div>
"""

content = content.replace(modals, "")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Reverted html modals successfully.")
