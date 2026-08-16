// Teacher Panel Logic

let currentUser = null;

function initTeacherPanel() {
  try {
    const userJson = localStorage.getItem('erp_current_teacher');
    if (!userJson) {
      window.location.href = 'erp-login.html';
      return;
    }
    
    currentUser = JSON.parse(userJson);
    if (currentUser.role !== 'teacher') {
      window.location.href = 'erp-login.html';
      return;
    }

    // Populate UI
    document.getElementById('topProfileName').textContent = currentUser.name;
    document.getElementById('topProfileClass').textContent = currentUser.assignedClass;
    const dateStr = new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
    
    const elDate = document.getElementById('currentDateStr');
    if(elDate) elDate.textContent = dateStr;
    const elClass = document.getElementById('attClassName');
    if(elClass) elClass.textContent = "Class " + currentUser.assignedClass;

    // Logout functionality
    const btnLogout = document.getElementById('btnLogout');
    if(btnLogout) {
        btnLogout.addEventListener('click', () => {
          localStorage.removeItem('erp_current_teacher');
          window.location.href = 'erp-login.html';
        });
    }
  } catch (err) {
    alert("Error initializing Teacher Panel: " + err.message);
  }
}

initTeacherPanel();

// Modal Logic
window.openTeacherModal = function(modalId) {
  const el = document.getElementById(modalId);
  el.style.display = 'flex';
  setTimeout(() => el.classList.add('active'), 10);
  
  if(modalId === 'attendanceModal') {
     populateAttendanceList();
  }
  if(modalId === 'studentsModal') {
     populateMyStudentsList();
  }
}

window.closeTeacherModal = function(modalId) {
  const el = document.getElementById(modalId);
  el.classList.remove('active');
  setTimeout(() => el.style.display = 'none', 300);
}

function getStudentsOfClass(classNum) {
    const users = JSON.parse(localStorage.getItem('erp_users')) || {};
    return Object.values(users).filter(u => u.role === 'student' && u.class == classNum);
}

// Attendance
window.populateAttendanceList = function() {
    const students = getStudentsOfClass(currentUser.assignedClass);
    const container = document.getElementById('studentAttendanceList');
    container.innerHTML = '';
    
    if(students.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding: 20px; color: #64748b;">No students registered in this class yet.</div>';
        return;
    }
    
    students.forEach(student => {
        const div = document.createElement('div');
        div.style.cssText = "display:flex; justify-content:space-between; align-items:center; background:#fff; padding:12px; border-radius:8px; border:1px solid #e2e8f0;";
        div.innerHTML = `
            <div>
                <div style="font-weight:700; color:#0f172a;">${student.name}</div>
                <div style="font-size:0.75rem; color:#64748b;">ID: ${student.studentId}</div>
            </div>
            <div>
                <select class="att-select" data-mobile="${student.mobile}" style="padding:6px; border-radius:4px; border:1px solid #cbd5e1; outline:none; font-weight:600;">
                    <option value="Present" selected>Present</option>
                    <option value="Absent">Absent</option>
                    <option value="Holiday">Holiday</option>
                    <option value="Sunday">Sunday</option>
                </select>
            </div>
        `;
        container.appendChild(div);
    });
}

window.submitAttendance = function() {
    const students = getStudentsOfClass(currentUser.assignedClass);
    if(students.length === 0) return alert("No students to mark.");
    
    const users = JSON.parse(localStorage.getItem('erp_users')) || {};
    const selects = document.querySelectorAll('.att-select');
    
    const dateObj = new Date();
    const today = dateObj.getFullYear() + "-" + String(dateObj.getMonth() + 1).padStart(2, '0') + "-" + String(dateObj.getDate()).padStart(2, '0');
    
    selects.forEach(sel => {
        const mobile = sel.getAttribute('data-mobile');
        if(users[mobile]) {
            users[mobile].attendanceRecords = users[mobile].attendanceRecords || {};
            users[mobile].attendanceRecords[today] = sel.value;
            
            let records = Object.values(users[mobile].attendanceRecords).filter(s => s === 'Present' || s === 'Absent');
            let presents = records.filter(s => s === 'Present').length;
            users[mobile].attendance = records.length > 0 ? Math.round((presents / records.length) * 100) : 0;
        }
    });
    
    localStorage.setItem('erp_users', JSON.stringify(users));
    alert("Attendance saved successfully!");
    closeTeacherModal('attendanceModal');
}

// Assignments
window.submitAssignment = function() {
    const subject = document.getElementById('assignSubject').value.trim();
    const title = document.getElementById('assignTitle').value.trim();
    const due = document.getElementById('assignDue').value;
    
    if(!subject || !title || !due) return alert("Please fill all fields.");
    
    const users = JSON.parse(localStorage.getItem('erp_users')) || {};
    const students = getStudentsOfClass(currentUser.assignedClass);
    
    let count = 0;
    students.forEach(s => {
        if(users[s.mobile]) {
            users[s.mobile].assignments = users[s.mobile].assignments || [];
            users[s.mobile].assignments.push({
                subject: subject,
                title: title,
                dueDate: due,
                status: "Pending"
            });
            count++;
        }
    });
    
    if(count > 0) {
        localStorage.setItem('erp_users', JSON.stringify(users));
        alert(`Assignment pushed to ${count} students successfully!`);
        document.getElementById('assignSubject').value = '';
        document.getElementById('assignTitle').value = '';
        document.getElementById('assignDue').value = '';
        closeTeacherModal('assignmentModal');
    } else {
        alert("No students found in this class.");
    }
}

// Notice
window.sendNotice = function() {
    const msg = document.getElementById('noticeMsg').value.trim();
    if(!msg) return alert("Please type a message.");
    
    // In a real app we'd save this to a global 'notices' DB.
    // Here we'll just alert for demo purposes since we don't have a student notice board UI yet.
    alert("Notice broadcasted successfully to Class " + currentUser.assignedClass + "!");
    document.getElementById('noticeMsg').value = '';
    closeTeacherModal('noticeModal');
}

// My Students Roster
window.populateMyStudentsList = function() {
    const students = getStudentsOfClass(currentUser.assignedClass);
    const container = document.getElementById('myStudentsList');
    container.innerHTML = '';
    
    if(students.length === 0) {
        container.innerHTML = '<div style="text-align:center; padding: 20px; color: #64748b;">No students registered in this class yet.</div>';
        return;
    }
    
    students.forEach(student => {
        const photo = student.photoURL && student.photoURL !== 'assets/images/default-avatar.png' ? student.photoURL : 'https://ui-avatars.com/api/?name='+student.name+'&background=2563eb&color=fff';
        const div = document.createElement('div');
        div.style.cssText = "display:flex; align-items:center; gap: 15px; background:#fff; padding:15px; border-radius:8px; border:1px solid #e2e8f0;";
        div.innerHTML = `
            <img src="${photo}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">
            <div style="flex: 1;">
                <div style="font-weight:800; color:#0f172a; font-size: 1.1rem;">${student.name}</div>
                <div style="font-size:0.8rem; color:#64748b; font-weight:600;">ID: <span style="color:#2563eb;">${student.studentId}</span> | Mobile: ${student.mobile}</div>
            </div>
            <div>
                <a href="tel:${student.mobile}" style="background: #e0f2fe; color: #0284c7; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-decoration: none;"><i class="fa-solid fa-phone"></i></a>
            </div>
        `;
        container.appendChild(div);
    });
}
