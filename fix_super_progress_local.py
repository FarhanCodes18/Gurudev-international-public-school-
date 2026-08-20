import re

file_path = r"d:\Gurudev international\Gurudev intenational\gurudev-super.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Modify the onSnapshot in gurudev-super.html to save to window
old_snapshot_logic = """        onSnapshot(q, (snapshot) => {
          if (snapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No students registered yet.</td></tr>';
            return;
          }
          tbody.innerHTML = '';
          snapshot.forEach((doc) => {
            const data = doc.data();"""

new_snapshot_logic = """        onSnapshot(q, (snapshot) => {
          window.superAdminAllStudents = [];
          if (snapshot.empty) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center;">No students registered yet.</td></tr>';
            return;
          }
          tbody.innerHTML = '';
          snapshot.forEach((doc) => {
            const data = doc.data();
            window.superAdminAllStudents.push(data);"""

if old_snapshot_logic in content:
    content = content.replace(old_snapshot_logic, new_snapshot_logic)


# 2. Modify the Progress logic to use window.superAdminAllStudents
old_progress_logic_start = """        studentSelect.innerHTML = '<option value="">Loading students from server...</option>';"""
old_progress_logic_end = """        }
      });
    }"""
    
# We will replace the entire try-catch block inside the change event with a local filter
old_progress_full = """        studentSelect.disabled = true;
        studentSelect.innerHTML = '<option value="">Loading students from server...</option>';
        
        try {
          // Fetch from Firebase students collection
          const q = query(collection(db, 'students'), where('class', '==', selectedClass));
          const snapshot = await getDocs(q);
          
          if(snapshot.empty) {
             studentSelect.innerHTML = '<option value="">No students found in this class</option>';
             studentSelect.disabled = true;
             studentSelect.style.background = '#f8fafc';
          } else {
             studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
             snapshot.forEach(docSnap => {
               const student = docSnap.data();
               studentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
             });
             studentSelect.disabled = false;
             studentSelect.style.background = '#ffffff';
          }
        } catch(err) {
          console.error("Error fetching students:", err);
          
          // Fallback to local storage if Firebase fails
          try {
            const users = JSON.parse(localStorage.getItem('erp_users')) || {};
            const allStudents = Object.values(users).filter(u => u.role === 'student');
            const filtered = allStudents.filter(s => s.class === selectedClass || s.class === "Class " + selectedClass);
            if(filtered.length === 0) {
               studentSelect.innerHTML = '<option value="">No students found</option>';
            } else {
               studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
               filtered.forEach(student => {
                 studentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
               });
               studentSelect.disabled = false;
               studentSelect.style.background = '#ffffff';
            }
          } catch(e) {
            studentSelect.innerHTML = '<option value="">Failed to load</option>';
          }
        }"""

new_progress_full = """        studentSelect.disabled = true;
        
        // Use globally loaded students from Firebase if available
        let allStudents = window.superAdminAllStudents || [];
        
        // Fallback to local storage if window array is empty
        if(allStudents.length === 0) {
            try {
                const users = JSON.parse(localStorage.getItem('erp_users')) || {};
                allStudents = Object.values(users).filter(u => u.role === 'student');
            } catch(e) {}
        }

        const filtered = allStudents.filter(s => String(s.class) === String(selectedClass) || s.class === "Class " + selectedClass);
        
        if(filtered.length === 0) {
           studentSelect.innerHTML = '<option value="">No students found in this class</option>';
           studentSelect.disabled = true;
           studentSelect.style.background = '#f8fafc';
        } else {
           studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
           filtered.forEach(student => {
             studentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
           });
           studentSelect.disabled = false;
           studentSelect.style.background = '#ffffff';
        }"""

if old_progress_full in content:
    content = content.replace(old_progress_full, new_progress_full)
else:
    print("WARNING: Could not find old progress block to replace.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed super admin progress by using local variables.")
