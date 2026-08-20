import re

file_path = r"d:\Gurudev international\Gurudev intenational\gurudev-super.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to replace the entire <script type="module"> block for Student Progress Logic
start_marker = "<!-- Student Progress Logic (Firebase) -->"
end_marker = "</script>"

start_idx = content.find(start_marker)
if start_idx != -1:
    end_idx = content.find(end_marker, start_idx)
    if end_idx != -1:
        end_idx += len(end_marker)
        old_block = content[start_idx:end_idx]
        
        new_block = """<!-- Student Progress Logic (Firebase) -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, addDoc, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

    const classSelect = document.getElementById('superProgressClassSelect');
    const studentSelect = document.getElementById('superProgressStudentSelect');
    const progressForm = document.getElementById('superProgressForm');
    const submitBtn = document.getElementById('superProgressSubmitBtn');

    if(classSelect && studentSelect) {
      classSelect.addEventListener('change', async () => {
        const selectedClass = classSelect.value;
        studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
        
        if(!selectedClass) {
          studentSelect.disabled = true;
          studentSelect.style.background = '#f8fafc';
          return;
        }
        
        studentSelect.disabled = true;
        studentSelect.innerHTML = '<option value="">Searching for students...</option>';
        
        try {
            // 1. Fetch from Firebase
            let allStudents = [];
            if(db) {
               try {
                  const querySnapshot = await getDocs(collection(db, 'students'));
                  querySnapshot.forEach((doc) => {
                     allStudents.push(doc.data());
                  });
               } catch(e) {
                  console.error("Firebase fetch error:", e);
               }
            }
            
            // 2. Fetch from LocalStorage as fallback
            try {
                const users = JSON.parse(localStorage.getItem('erp_users')) || {};
                const localStudents = Object.values(users).filter(u => u.role === 'student');
                localStudents.forEach(ls => {
                   // Avoid duplicates if Firebase already fetched them
                   if(!allStudents.find(fs => fs.studentId === ls.studentId)) {
                       allStudents.push(ls);
                   }
                });
            } catch(e) {
                console.error("Local storage error:", e);
            }
            
            // 3. Filter by class (robust matching)
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
               studentSelect.innerHTML = '<option value="">No students found in this class</option>';
               studentSelect.disabled = true;
               studentSelect.style.background = '#f8fafc';
            } else {
               studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
               filtered.forEach(student => {
                 studentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId || 'No ID'})</option>`;
               });
               studentSelect.disabled = false;
               studentSelect.style.background = '#ffffff';
            }
        } catch(err) {
            console.error("Overall error:", err);
            studentSelect.innerHTML = '<option value="">Error loading students</option>';
        }
      });
    }

    if(progressForm) {
      progressForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
        submitBtn.disabled = true;
        
        const studentId = studentSelect.value;
        const studentName = studentSelect.options[studentSelect.selectedIndex].text.split('(')[0].trim();
        const className = classSelect.value;
        const progressText = document.getElementById('superProgressText').value;
        
        try {
          await addDoc(collection(db, 'student_progress'), {
            studentId: studentId,
            studentName: studentName,
            className: className,
            progressText: progressText,
            timestamp: Date.now(),
            dateStr: new Date().toISOString()
          });
          
          if(typeof showCustomAlert === 'function') {
             showCustomAlert("Success", "Progress report successfully uploaded to student portal!", "success");
          } else {
             alert('Progress report successfully uploaded to student portal!');
          }
          
          progressForm.reset();
          studentSelect.disabled = true;
          studentSelect.style.background = '#f8fafc';
        } catch(err) {
          console.error("Error uploading progress:", err);
          if(typeof showCustomAlert === 'function') {
             showCustomAlert("Error", "Failed to upload progress. Check console.", "error");
          } else {
             alert('Failed to upload progress.');
          }
        } finally {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
        }
      });
    }
  </script>"""
        
        content = content.replace(old_block, new_block)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Updated student progress logic in gurudev-super.html successfully.")
else:
    print("Could not find start marker.")
