import re

file_path = r"d:\Gurudev international\Gurudev intenational\gurudev-super.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_script = """  <!-- Student Progress Logic (Firebase) -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, addDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

    const classSelect = document.getElementById('superProgressClassSelect');
    const studentSelect = document.getElementById('superProgressStudentSelect');
    const progressForm = document.getElementById('superProgressForm');
    const submitBtn = document.getElementById('superProgressSubmitBtn');

    if(classSelect && studentSelect) {
      classSelect.addEventListener('change', () => {
        const selectedClass = classSelect.value;
        studentSelect.innerHTML = '<option value="">-- Choose Student --</option>';
        
        if(!selectedClass) {
          studentSelect.disabled = true;
          studentSelect.style.background = '#f8fafc';
          return;
        }
        
        const students = JSON.parse(localStorage.getItem('erp_students')) || [];
        const filtered = students.filter(s => s.class === selectedClass);
        
        if(filtered.length === 0) {
           studentSelect.innerHTML = '<option value="">No students found in this class</option>';
           studentSelect.disabled = true;
           studentSelect.style.background = '#f8fafc';
        } else {
           filtered.forEach(student => {
             studentSelect.innerHTML += `<option value="${student.studentId}">${student.name} (${student.studentId})</option>`;
           });
           studentSelect.disabled = false;
           studentSelect.style.background = '#ffffff';
        }
      });
    }"""

new_script = """  <!-- Student Progress Logic (Firebase) -->
  <script type="module">
    import { db } from './js/firebase-config.js';
    import { collection, addDoc, query, where, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

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
        }
      });
    }"""

if old_script in content:
    content = content.replace(old_script, new_script)
else:
    print("WARNING: Could not find old script to replace.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed student fetching in gurudev-super.html")
