import re
import os

file_path = r"d:\Gurudev international\Gurudev intenational\js\erp-admin.js"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the progress logic in erp-admin.js
old_logic = """    if(window.allStudentsData && window.allStudentsData.length > 0) {
      const filtered = window.allStudentsData.filter(s => s.class === selectedClass);
      if(filtered.length === 0) {
         progressStudentSelect.innerHTML = '<option value="">No students in this class</option>';
      } else {
         filtered.forEach(student => {
           progressStudentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
         });
         progressStudentSelect.disabled = false;
      }
    } else {
      // Mock mode fallback
      progressStudentSelect.innerHTML += `<option value="GI20261001">Rahul Sharma (GI20261001)</option>`;
      progressStudentSelect.innerHTML += `<option value="GI20261002">Priya Singh (GI20261002)</option>`;
      progressStudentSelect.disabled = false;
    }"""

new_logic = """    
    progressStudentSelect.disabled = true;
    progressStudentSelect.innerHTML = '<option value="">Searching for students...</option>';
    
    // Fallback if window.allStudentsData is missing or empty
    let allStudents = window.allStudentsData || [];
    if(allStudents.length === 0) {
        try {
            const users = JSON.parse(localStorage.getItem('erp_users')) || {};
            allStudents = Object.values(users).filter(u => u.role === 'student');
        } catch(e) {}
    }
    
    const filtered = allStudents.filter(s => {
        if(!s.class) return false;
        const sClass = String(s.class).trim().toLowerCase();
        const selClass = String(selectedClass).trim().toLowerCase();
        return sClass === selClass || 
               sClass === "class " + selClass || 
               sClass === "class" + selClass ||
               sClass === "0" + selClass;
    });

    if(filtered.length === 0) {
       progressStudentSelect.innerHTML = '<option value="">No students found in this class</option>';
       progressStudentSelect.disabled = true;
    } else {
       progressStudentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
       filtered.forEach(student => {
         progressStudentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId || 'No ID'})</option>`;
       });
       progressStudentSelect.disabled = false;
    }"""

if old_logic in content:
    content = content.replace(old_logic, new_logic)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed progress logic in erp-admin.js")
else:
    print("WARNING: Could not find old logic in erp-admin.js")
