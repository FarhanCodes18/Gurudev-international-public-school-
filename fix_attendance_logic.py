import re

file_path = r"d:\Gurudev international\Gurudev intenational\js\erp-student.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_logic = """      let records = freshUser.attendanceRecords || {};
      let recordKeys = Object.keys(records).sort().reverse(); // Newest first
      
      let presents = 0;
      let total = recordKeys.length;
      
      let listHTML = '';
      if(total === 0) {
        listHTML = `<p style="color:#94a3b8; font-size:0.85rem; margin-top:16px;"><i class="fa-solid fa-circle-info"></i> Attendance tracking hasn't started for your profile yet.</p>`;
      } else {
        recordKeys.forEach(date => {
          let status = records[date];
          if(status === 'Present') presents++;
          
          let color = status === 'Present' ? '#10b981' : (status === 'Absent' ? '#ef4444' : '#f59e0b');
          let bg = status === 'Present' ? '#f0fdf4' : (status === 'Absent' ? '#fef2f2' : '#fff7ed');
          
          listHTML += `<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 16px; background:${bg}; border-left:4px solid ${color}; border-radius:8px; margin-bottom:10px;">
            <div style="font-weight:600; color:#334155;">${date}</div>
            <div style="font-weight:700; color:${color}; font-size:0.9rem; text-transform:uppercase;">${status}</div>
          </div>`;
        });
      }
      
      let percentage = total > 0 ? Math.round((presents / total) * 100) : 0;"""


new_logic = """      let records = freshUser.attendanceRecords || {};
      let recordKeys = Object.keys(records).sort().reverse(); // Newest first
      
      let presents = 0;
      let totalWorkingDays = 0;
      let total = recordKeys.length;
      
      let listHTML = '';
      if(total === 0) {
        listHTML = `<p style="color:#94a3b8; font-size:0.85rem; margin-top:16px;"><i class="fa-solid fa-circle-info"></i> Attendance tracking hasn't started for your profile yet.</p>`;
      } else {
        recordKeys.forEach(date => {
          let status = records[date];
          
          if(status !== 'Holiday') {
            totalWorkingDays++;
            if(status === 'Present') presents++;
          }
          
          let color = status === 'Present' ? '#10b981' : (status === 'Absent' ? '#ef4444' : (status === 'Holiday' ? '#3b82f6' : '#f59e0b'));
          let bg = status === 'Present' ? '#f0fdf4' : (status === 'Absent' ? '#fef2f2' : (status === 'Holiday' ? '#eff6ff' : '#fff7ed'));
          
          listHTML += `<div style="display:flex; justify-content:space-between; align-items:center; padding:12px 16px; background:${bg}; border-left:4px solid ${color}; border-radius:8px; margin-bottom:10px;">
            <div style="font-weight:600; color:#334155;">${date}</div>
            <div style="font-weight:700; color:${color}; font-size:0.9rem; text-transform:uppercase;">${status}</div>
          </div>`;
        });
      }
      
      let percentage = totalWorkingDays > 0 ? Math.round((presents / totalWorkingDays) * 100) : 0;"""


if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed attendance logic in erp-student.js")
else:
    print("WARNING: Could not find old logic in erp-student.js")
