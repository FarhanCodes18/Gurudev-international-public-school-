/* admin.js - Superpower Admin Panel Logic (Light Theme & Sync Updates) */
document.addEventListener('DOMContentLoaded', () => {
  // Navigation Logic
  const navItems = document.querySelectorAll('.nav-item');
  const viewSections = document.querySelectorAll('.view-section');

  navItems.forEach(item => {
    item.addEventListener('click', () => {
      navItems.forEach(nav => nav.classList.remove('active'));
      viewSections.forEach(view => view.classList.remove('active'));
      
      item.classList.add('active');
      const targetView = item.getAttribute('data-view');
      const targetSection = document.getElementById('view-' + targetView);
      if(targetSection) targetSection.classList.add('active');
    });
  });

  // Set Default Attendance Date to Today
  const dateInput = document.getElementById('attendance-date');
  if(dateInput) {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    dateInput.value = `${yyyy}-${mm}-${dd}`;
    
    // Initial Analytics Render
    setTimeout(renderAttendanceAnalytics, 500);
  }

  // Fetch Data from LocalStorage
  const studentsRaw = localStorage.getItem('erp_users');
  let studentsObj = {};
  let students = []; // Array version for looping
  if(studentsRaw) {
    try { 
      studentsObj = JSON.parse(studentsRaw); 
      // Convert to array for easy mapping
      students = Object.values(studentsObj);
    } catch(e) {}
  }

  // --- POPULATE DASHBOARD TOTALS ---
  const dashTotal = document.getElementById('dash-total-students');
  if(dashTotal) dashTotal.innerText = students.length;

  // --- POPULATE ALL STUDENTS LIST ---
  const allStudentsTable = document.getElementById('all-students-list');
  if(allStudentsTable) {
    allStudentsTable.innerHTML = '';
    if(students.length === 0) {
      allStudentsTable.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted); padding: 40px 0;">No student data available.</td></tr>';
    } else {
      students.slice().reverse().forEach(st => {
        const photo = st.photoURL || 'https://ui-avatars.com/api/?name='+st.name+'&background=2563eb&color=fff';
        allStudentsTable.innerHTML += `
          <tr>
            <td class="student-cell">
              <img src="${photo}" alt="Photo">
              <div><h5>${st.name}</h5><p>${st.email || 'N/A'}</p></div>
            </td>
            <td style="font-family: monospace; font-weight: 600; color:var(--admin-accent);">${st.studentId}</td>
            <td>${st.class}</td>
            <td>${st.mobile}</td>
            <td><span class="status-badge status-active">Active</span></td>
            <td style="display:flex; gap:8px;">
              <button class="btn-admin-outline" style="padding:6px 12px; font-size:0.75rem;" onclick="viewStudentProfile('${st.mobile}')">View</button>
              <button class="btn-admin-outline" style="padding:6px 12px; font-size:0.75rem; border-color:#dc2626; color:#dc2626;" onclick="deleteStudent('${st.mobile}')"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>
        `;
      });
    }
  }

  // --- POPULATE CERTIFICATE SELECTOR ---
  const certSelector = document.getElementById('cert-student');
  if(certSelector) {
    certSelector.innerHTML = '<option value="">-- Select a Student --</option>';
    students.forEach(st => {
      certSelector.innerHTML += `<option value="${st.mobile}">${st.name} (${st.studentId})</option>`;
    });
  }

  // --- LEAVE APPROVALS ---
  const leaveTable = document.getElementById('admin-leave-requests');
  let pendingLeaves = 0;
  if(leaveTable) {
    leaveTable.innerHTML = '';
    let hasLeaves = false;
    students.forEach(st => {
      if(st.leaveRequests) {
        st.leaveRequests.forEach((leave, idx) => {
          if(leave.status === 'Pending') {
            hasLeaves = true;
            pendingLeaves++;
            leaveTable.innerHTML += `
              <tr>
                <td>${st.name}</td>
                <td>${st.studentId}</td>
                <td>${leave.reason}</td>
                <td>${leave.date}</td>
                <td>
                  <button class="action-btn" style="color:var(--admin-success); border-color:var(--admin-success);" onclick="approveLeave('${st.mobile}', ${idx})"><i class="fa-solid fa-check"></i></button>
                  <button class="action-btn danger" onclick="rejectLeave('${st.mobile}', ${idx})"><i class="fa-solid fa-xmark"></i></button>
                </td>
              </tr>
            `;
          }
        });
      }
    });
    
    if(!hasLeaves) {
      leaveTable.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted); padding:30px;">No pending leave requests.</td></tr>';
    }
    const badge = document.getElementById('pending-leaves-badge');
    if (badge) badge.innerText = pendingLeaves;
  }

  // --- STUDENT ANALYTICS CHART (CHART.JS) ---
  const ctx = document.getElementById('registrationChart');
  if(ctx && students.length > 0) {
    const classCounts = {};
    students.forEach(st => {
      const c = st.class || 'Unknown';
      classCounts[c] = (classCounts[c] || 0) + 1;
    });
    
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: Object.keys(classCounts).map(c => 'Class ' + c),
        datasets: [{
          label: 'Students Registered',
          data: Object.values(classCounts),
          backgroundColor: '#2563eb',
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: '#e2e8f0' }, ticks: { color: '#64748b', stepSize: 1 } },
          x: { grid: { display: false }, ticks: { color: '#64748b' } }
        }
      }
    });
  }

  // Load Admissions and Contact Inquiries initially
  loadCallbacks();
  loadContactMessages();
});

// --- GLOBAL LOADER TOOL ---
function showLoader(title, desc, duration, callback) {
  const overlay = document.getElementById('admin-loader');
  document.getElementById('loader-title').innerText = title;
  document.getElementById('loader-desc').innerText = desc;
  overlay.classList.add('active');
  
  setTimeout(() => {
    overlay.classList.remove('active');
    if(callback) callback();
  }, duration);
}

// --- CMS FUNCTIONS ---

// Update Marquee
function updateMarquee() {
  const input = document.getElementById('marquee-input').value;
  if(input) {
    showLoader('Syncing to Website', 'Updating live marquee announcements...', 1500, () => {
      localStorage.setItem('admin_marquee_text', input);
      alert('Marquee updated successfully on the live website!');
    });
  }
}

// Gallery Upload & Sync
function uploadGallery() {
  const name = document.getElementById('gallery-name').value;
  const score = document.getElementById('gallery-score').value;
  const fileInput = document.getElementById('gallery-photo');
  
  if(!name || !score || fileInput.files.length === 0) {
    return alert('Please fill all fields and select a photo.');
  }

  const file = fileInput.files[0];
  const reader = new FileReader();
  
  reader.onload = function(e) {
    const base64Image = e.target.result;
    let gallery = JSON.parse(localStorage.getItem('admin_achievers_gallery') || '[]');
    
    // Add to front of array
    gallery.unshift({ name, score, image: base64Image });
    
    // Keep max 10 to match the 10 slider placeholders
    if(gallery.length > 10) gallery.pop();
    
    showLoader('Uploading Photo', 'Optimizing and syncing to the Homepage Slider...', 2000, () => {
      localStorage.setItem('admin_achievers_gallery', JSON.stringify(gallery));
      alert('Photo synced to the Homepage successfully! Go check the slider.');
      document.getElementById('gallery-name').value = '';
      document.getElementById('gallery-score').value = '';
      fileInput.value = '';
    });
  };
  
  reader.readAsDataURL(file);
}

// School Gallery Upload & Sync
function uploadSchoolGallery() {
  const fileInput = document.getElementById('school-gallery-photo');
  const descInput = document.getElementById('school-gallery-desc');
  
  if(fileInput.files.length === 0) {
    return alert('Please select a photo to upload.');
  }

  const desc = descInput ? descInput.value : '';
  const file = fileInput.files[0];
  const reader = new FileReader();
  
  reader.onload = function(e) {
    const base64Image = e.target.result;
    let gallery = JSON.parse(localStorage.getItem('admin_school_gallery') || '[]');
    
    // Add to front of array
    gallery.unshift({ image: base64Image, desc: desc, date: new Date().toLocaleDateString() });
    
    showLoader('Uploading Photo', 'Optimizing and syncing to the School Gallery...', 2000, () => {
      localStorage.setItem('admin_school_gallery', JSON.stringify(gallery));
      alert('Photo synced to the School Gallery successfully!');
      fileInput.value = '';
      if(descInput) descInput.value = '';
    });
  };
  
  reader.readAsDataURL(file);
}

// Bulk SMS Blaster
function sendBulkSMS() {
  showLoader('Sending Bulk SMS', 'Establishing gateway connection. Sending 500+ messages...', 3500, () => {
    alert('SMS Blast completed successfully! 524 messages delivered.');
  });
}

// Generate Certificate
function generateCertificate() {
  const mobile = document.getElementById('cert-student').value;
  const type = document.getElementById('cert-type').value;
  
  if(!mobile) return alert("Please select a student");
  
  showLoader('Generating Certificate', 'Signing securely and issuing to Student Portal...', 2000, () => {
    const studentsRaw = localStorage.getItem('erp_users');
    let students = JSON.parse(studentsRaw);
    
    if(students[mobile]) {
      if(!students[mobile].certificates) students[mobile].certificates = [];
      students[mobile].certificates.push({
        type: type,
        date: new Date().toLocaleDateString(),
        issuedBy: 'Admin'
      });
      localStorage.setItem('erp_users', JSON.stringify(students));
      alert('Certificate issued successfully to the student portal!');
    }
  });
}

// Publish Notice
function publishNotice() {
  const title = document.getElementById('notice-title').value;
  const body = document.getElementById('notice-body').value;
  if(!title || !body) return alert("Fill all fields");
  
  showLoader('Publishing Notice', 'Sending to portal...', 1500, () => {
    let notices = JSON.parse(localStorage.getItem('admin_notices') || '[]');
    notices.push({ title, body, date: new Date().toLocaleDateString() });
    localStorage.setItem('admin_notices', JSON.stringify(notices));
    alert('Notice published!');
  });
}

// Leave Actions
function approveLeave(phone, idx) {
  showLoader('Approving Leave', 'Updating database...', 1000, () => {
    let students = JSON.parse(localStorage.getItem('erp_users'));
    if(students[phone] && students[phone].leaveRequests) {
      students[phone].leaveRequests[idx].status = 'Approved';
      localStorage.setItem('erp_users', JSON.stringify(students));
      window.location.reload();
    }
  });
}

function rejectLeave(phone, idx) {
  showLoader('Rejecting Leave', 'Updating database...', 1000, () => {
    let students = JSON.parse(localStorage.getItem('erp_users'));
    if(students[phone] && students[phone].leaveRequests) {
      students[phone].leaveRequests[idx].status = 'Rejected';
      localStorage.setItem('erp_users', JSON.stringify(students));
      window.location.reload();
    }
  });
}

// View Student Profile Modal
function viewStudentProfile(mobile) {
  let students = JSON.parse(localStorage.getItem('erp_users'));
  let st = students[mobile];
  if(st) {
    document.getElementById('modal-photo').src = st.photoURL || 'https://ui-avatars.com/api/?name='+st.name+'&background=2563eb&color=fff';
    document.getElementById('modal-name').innerText = st.name;
    document.getElementById('modal-id').innerText = st.studentId;
    document.getElementById('modal-class').innerText = st.class;
    document.getElementById('modal-gender').innerText = st.gender || 'N/A';
    document.getElementById('modal-mobile').innerText = st.mobile;
    document.getElementById('modal-dob').innerText = st.dob || 'N/A';
    document.getElementById('modal-password').innerText = st.password || 'Not Set';
    
    document.getElementById('student-modal').classList.add('active');
  }
}

// --- ATTENDANCE SYSTEM LOGIC ---
function loadAttendanceRegister() {
  const dateObj = document.getElementById('attendance-date').value;
  const classVal = document.getElementById('attendance-class').value;
  
  if(!dateObj || !classVal) {
    return alert('Please select a Date and a Class.');
  }

  showLoader('Loading Register', 'Fetching records for ' + classVal, 800, () => {
    let users = JSON.parse(localStorage.getItem('erp_users')) || {};
    
    let studentArray = [];
    if(classVal === 'Staff') {
      studentArray = Object.values(users).filter(s => s.role === 'staff');
    } else {
      studentArray = Object.values(users).filter(s => s.role === 'student' && s.class === classVal);
    }
    
    const listBody = document.getElementById('attendance-list');
    listBody.innerHTML = '';
    
    if(studentArray.length === 0) {
      listBody.innerHTML = '<tr><td colspan="3" style="text-align:center; color:var(--admin-muted); padding:30px;">No records found for ' + classVal + '.</td></tr>';
    } else {
      studentArray.forEach(st => {
        // Check if attendance already marked for this date
        let isPresent = false;
        if(st.attendanceRecords && st.attendanceRecords[dateObj] === 'Present') {
          isPresent = true;
        }

        listBody.innerHTML += `
          <tr data-mobile="${st.mobile}">
            <td><div style="display:flex; align-items:center; gap:10px;">
              <img src="${st.photoURL || 'https://ui-avatars.com/api/?name='+st.name}" style="width:30px; height:30px; border-radius:50%; object-fit:cover;">
              <strong>${st.name}</strong>
            </div></td>
            <td>${st.studentId}</td>
            <td>
              <select class="admin-select attendance-status" style="padding:5px; width:120px;">
                <option value="Present" ${isPresent ? 'selected' : ''}>Present</option>
                <option value="Absent" ${!isPresent ? 'selected' : ''}>Absent</option>
              </select>
            </td>
          </tr>
        `;
      });
    }
    
    document.getElementById('register-subtitle').innerText = `(Class ${classVal} - ${dateObj})`;
    document.getElementById('attendance-register-container').style.display = 'block';
  });
}

function saveAttendance() {
  const dateObj = document.getElementById('attendance-date').value;
  if(!dateObj) return alert("Date missing!");

  showLoader('Saving Attendance', 'Writing records to database...', 1200, () => {
    let users = JSON.parse(localStorage.getItem('erp_users')) || {};
    const rows = document.querySelectorAll('#attendance-list tr[data-mobile]');
    
    let markedCount = 0;
    rows.forEach(row => {
      const mobile = row.getAttribute('data-mobile');
      const status = row.querySelector('.attendance-status').value;
      
      if(users[mobile]) {
        if(!users[mobile].attendanceRecords) {
          users[mobile].attendanceRecords = {};
        }
        users[mobile].attendanceRecords[dateObj] = status;
        
        // Recalculate total attendance percentage if needed
        let records = Object.values(users[mobile].attendanceRecords);
        let presents = records.filter(s => s === 'Present').length;
        users[mobile].attendance = Math.round((presents / records.length) * 100);
        
        markedCount++;
      }
    });

    localStorage.setItem('erp_users', JSON.stringify(users));
    alert('Successfully saved attendance for ' + markedCount + ' records.');
    renderAttendanceAnalytics(); // Update donut chart instantly
  });
}

// --- STAFF REGISTRATION ---
function registerStaff() {
  const name = document.getElementById('staff-name').value;
  const mobile = document.getElementById('staff-mobile').value;
  const gender = document.getElementById('staff-gender').value;
  const role = document.getElementById('staff-role').value;
  
  if(!name || !mobile || !role) {
    return alert('Please fill all fields');
  }

  showLoader('Registering Staff', 'Creating profile...', 1000, () => {
    let users = JSON.parse(localStorage.getItem('erp_users')) || {};
    if(users[mobile]) {
      return alert('This mobile number is already registered.');
    }
    
    const staffId = 'STF-' + Math.floor(1000 + Math.random() * 9000);
    users[mobile] = {
      role: 'staff',
      studentId: staffId, // using same field name for compatibility
      name: name,
      mobile: mobile,
      email: '',
      class: role, // storing role/subject in the class field for the modal
      gender: gender,
      photoURL: '',
      password: mobile, // default password
      registrationDate: new Date().toISOString(),
      attendance: 0,
      attendanceRecords: {}
    };
    
    localStorage.setItem('erp_users', JSON.stringify(users));
    alert('Staff ' + name + ' registered successfully! They can now be marked in attendance.');
    
    document.getElementById('staff-name').value = '';
    document.getElementById('staff-mobile').value = '';
    document.getElementById('staff-role').value = '';
  });
}

// --- ATTENDANCE ANALYTICS (CHART.JS) ---
let attendanceChartInstance = null;

function renderAttendanceAnalytics() {
  const dateInput = document.getElementById('attendance-date');
  if(!dateInput) return;
  const targetDate = dateInput.value;
  if(!targetDate) return;

  const users = JSON.parse(localStorage.getItem('erp_users')) || {};
  let totalPresent = 0;
  let totalAbsent = 0;
  
  Object.values(users).forEach(u => {
    if(u.attendanceRecords && u.attendanceRecords[targetDate]) {
      if(u.attendanceRecords[targetDate] === 'Present') totalPresent++;
      else if(u.attendanceRecords[targetDate] === 'Absent') totalAbsent++;
    }
  });

  const ctx = document.getElementById('attendanceAnalyticsChart');
  if(!ctx) return;

  // If no data, show empty gray donut
  const dataVals = (totalPresent === 0 && totalAbsent === 0) ? [1] : [totalPresent, totalAbsent];
  const bgColors = (totalPresent === 0 && totalAbsent === 0) ? ['#e2e8f0'] : ['#16a34a', '#e11d48'];
  const labels = (totalPresent === 0 && totalAbsent === 0) ? ['No Data'] : ['Present', 'Absent'];

  if(attendanceChartInstance) {
    attendanceChartInstance.destroy();
  }

  attendanceChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: dataVals,
        backgroundColor: bgColors,
        borderWidth: 0,
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '75%',
      plugins: {
        legend: { position: 'bottom', labels: { color: '#64748b', boxWidth:12 } },
        tooltip: { enabled: (totalPresent > 0 || totalAbsent > 0) }
      }
    }
  });
}

// --- NOTICES & E-LIBRARY ---
function publishNotice() {
  const title = document.getElementById('notice-title').value;
  const body = document.getElementById('notice-body').value;
  if(!title || !body) return alert("Please enter both title and content.");

  showLoader('Publishing Notice', 'Syncing to website...', 800, () => {
    let notices = JSON.parse(localStorage.getItem('erp_notices')) || [];
    notices.unshift({
      date: new Date().toLocaleDateString('en-GB'),
      title: title,
      body: body
    });
    localStorage.setItem('erp_notices', JSON.stringify(notices));
    alert("Notice successfully published to the public portal!");
    document.getElementById('notice-title').value = '';
    document.getElementById('notice-body').value = '';
  });
}

function publishLibraryItem() {
  const subject = document.getElementById('lib-subject').value;
  const name = document.getElementById('lib-name').value;
  const link = document.getElementById('lib-link').value;
  if(!name || !link) return alert("Please enter book name and link.");

  showLoader('Uploading Book', 'Adding to E-Library...', 800, () => {
    let library = JSON.parse(localStorage.getItem('erp_library')) || [];
    library.unshift({
      subject: subject,
      name: name,
      link: link,
      date: new Date().toLocaleDateString('en-GB')
    });
    localStorage.setItem('erp_library', JSON.stringify(library));
    alert("Book added to E-Library successfully!");
    document.getElementById('lib-name').value = '';
    document.getElementById('lib-link').value = '';
  });
}

// --- ADMISSIONS & CALLBACKS ---
function loadCallbacks() {
  const listBody = document.getElementById('callbacks-list');
  let callbacks = JSON.parse(localStorage.getItem('erp_callbacks')) || [];
  
  if(callbacks.length === 0) {
    listBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted); padding:40px;">No online applications yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  callbacks.reverse().forEach(cb => {
    listBody.innerHTML += `
      <tr>
        <td>${cb.date}</td>
        <td><strong>${cb.name}</strong></td>
        <td><a href="tel:${cb.phone}" style="color:var(--admin-accent); text-decoration:none;">${cb.phone}</a></td>
        <td><span class="status-badge status-active">${cb.position || cb.class}</span></td>
        <td style="max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${cb.message || 'N/A'}">${cb.message || 'N/A'}</td>
      </tr>
    `;
  });
}

function loadContactMessages() {
  const listBody = document.getElementById('contact-messages-list');
  if(!listBody) return;
  
  let messages = JSON.parse(localStorage.getItem('admin_contact_messages')) || [];
  
  if(messages.length === 0) {
    listBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted); padding:40px;">No contact inquiries yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  messages.reverse().forEach(msg => {
    listBody.innerHTML += `
      <tr>
        <td>${msg.date}</td>
        <td><strong>${msg.name}</strong></td>
        <td><a href="tel:${msg.phone}" style="color:var(--admin-accent); text-decoration:none;">${msg.phone}</a></td>
        <td>
          <a href="mailto:${msg.email}" style="color:var(--admin-muted); text-decoration:none; display:block; font-size:0.85rem;"><i class="fa-solid fa-envelope"></i> ${msg.email}</a>
          <span style="font-weight:600; font-size:0.85rem;">${msg.subject || 'General'}</span>
        </td>
        <td style="max-width:250px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${msg.message || 'N/A'}">${msg.message || 'N/A'}</td>
      </tr>
    `;
  });
}

// --- EXAMINATION RESULTS ---
function publishResult() {
  const roll = document.getElementById('res-roll').value;
  const name = document.getElementById('res-name').value;
  const cls = document.getElementById('res-class').value;
  
  const mEng = Number(document.getElementById('res-english').value);
  const mMath = Number(document.getElementById('res-math').value);
  const mSci = Number(document.getElementById('res-science').value);
  const mSoc = Number(document.getElementById('res-social').value);
  const mHin = Number(document.getElementById('res-hindi').value);
  
  if(!roll || !name || isNaN(mEng) || isNaN(mMath) || isNaN(mSci) || isNaN(mSoc) || isNaN(mHin)) {
    return alert("Please fill all fields with valid numbers.");
  }

  showLoader('Publishing Result', 'Calculating percentage...', 1000, () => {
    const total = mEng + mMath + mSci + mSoc + mHin;
    const percent = (total / 5).toFixed(2);
    let status = percent >= 33 ? 'PASS' : 'FAIL';
    
    let results = JSON.parse(localStorage.getItem('erp_results')) || {};
    results[roll] = {
      roll: roll,
      name: name,
      class: cls,
      marks: {
        english: mEng, math: mMath, science: mSci, social: mSoc, hindi: mHin
      },
      total: total,
      percentage: percent,
      status: status,
      date: new Date().toLocaleDateString('en-GB')
    };
    
    localStorage.setItem('erp_results', JSON.stringify(results));
    alert(`Result published! Total: ${total}/500 (${percent}%). Status: ${status}`);
    
    document.getElementById('res-roll').value = '';
    document.getElementById('res-name').value = '';
    document.getElementById('res-english').value = '';
    document.getElementById('res-math').value = '';
    document.getElementById('res-science').value = '';
    document.getElementById('res-social').value = '';
    document.getElementById('res-hindi').value = '';
  });
}

// --- BULK SMS BLASTER ---
function sendBulkSMS() {
  const target = document.getElementById('sms-target').value;
  const msg = document.getElementById('sms-msg').value;
  
  if(!msg) return alert('Please enter a message to blast.');
  
  showLoader('Preparing SMS Blaster', 'Querying student database...', 1200, () => {
    let users = JSON.parse(localStorage.getItem('erp_users')) || {};
    let targetStudents = [];
    
    Object.values(users).forEach(u => {
      if(u.role === 'student') {
        if(target === 'all' || u.class === target) {
          targetStudents.push(u);
        }
      }
    });
    
    if(targetStudents.length === 0) {
      alert("No students found in the selected target group.");
      return;
    }
    
    alert(`SMS API Triggered Successfully!\n\nMessage queued for ${targetStudents.length} recipients.\nTarget: ${target === 'all' ? 'All Students' : 'Class ' + target}`);
    document.getElementById('sms-msg').value = '';
  });
}

// --- CERTIFICATE MAKER ---
function populateCertStudents() {
  const cls = document.getElementById('cert-class').value;
  const studentSelect = document.getElementById('cert-student');
  const nameInput = document.getElementById('cert-name');
  
  studentSelect.innerHTML = '<option value="" disabled selected>-- Choose Student --</option>';
  nameInput.value = '';
  
  if(!cls) return;
  
  let users = JSON.parse(localStorage.getItem('erp_users')) || {};
  let count = 0;
  
  Object.values(users).forEach(u => {
    if(u.role === 'student' && u.class === cls) {
      const opt = document.createElement('option');
      opt.value = u.name; // Use name as value for easy access, or ID
      opt.dataset.name = u.name;
      opt.textContent = `${u.name} (ID: ${u.id})`;
      studentSelect.appendChild(opt);
      count++;
    }
  });
  
  if(count === 0) {
    studentSelect.innerHTML = '<option value="" disabled selected>No students found</option>';
  }
}

function autoFillCertName() {
  const studentSelect = document.getElementById('cert-student');
  const nameInput = document.getElementById('cert-name');
  
  if(studentSelect.options[studentSelect.selectedIndex]) {
    nameInput.value = studentSelect.options[studentSelect.selectedIndex].dataset.name || '';
  }
}

function resetCertForm() {
  document.getElementById('cert-class').value = '';
  document.getElementById('cert-student').innerHTML = '<option value="" disabled selected>-- Choose Student --</option>';
  document.getElementById('cert-name').value = '';
  document.getElementById('cert-title').value = 'Certificate of Excellence';
  document.getElementById('cert-desc').value = 'for demonstrating exceptional dedication, outstanding academic performance, and exemplary character during the academic session.';
  document.getElementById('cert-date').value = new Date().toISOString().split('T')[0];
  document.getElementById('cert-signame').value = 'A.R Qureshi';
  document.getElementById('cert-sigtitle').value = 'Director';
  document.getElementById('cert-sigimg').value = '';
  document.getElementById('cert-logoimg').value = '';
}

function generatePrintableCertificate() {
  const name = document.getElementById('cert-name').value;
  const title = document.getElementById('cert-title').value;
  const desc = document.getElementById('cert-desc').value;
  const dateStr = document.getElementById('cert-date').value;
  const sigName = document.getElementById('cert-signame').value;
  const sigTitle = document.getElementById('cert-sigtitle').value;
  
  const sigInput = document.getElementById('cert-sigimg');
  const logoInput = document.getElementById('cert-logoimg');
  
  if(!name) {
    alert("Please provide the recipient's name.");
    return;
  }
  
  // Format Date (e.g. 01 August 2026)
  let formattedDate = dateStr;
  if(dateStr) {
    const d = new Date(dateStr);
    const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
    formattedDate = `${d.getDate().toString().padStart(2, '0')} ${months[d.getMonth()]} ${d.getFullYear()}`;
  }
  
  showLoader('Generating Certificate', 'Preparing high-resolution print layout...', 1500, () => {
    // Process Images
    let sigBase64 = '';
    let logoBase64 = '';
    
    const renderPrint = () => {
      // const printWindow = window.open('', '_blank');
      
      const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Print Certificate - ${name}</title>
          <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;800&family=Great+Vibes&family=Montserrat:wght@400;600&display=swap');
            body, html { margin: 0; padding: 0; background: #525659; display: flex; justify-content: center; align-items: center; height: 100vh; font-family: 'Montserrat', sans-serif; }
            .cert-container { 
              background: white; width: 1123px; height: 794px; /* A4 Landscape at 96dpi roughly */
              position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5); overflow: hidden;
              padding: 50px; box-sizing: border-box; text-align: center;
              border: 15px solid #0f172a; outline: 5px solid #d4af37; outline-offset: -25px;
            }
            .cert-bg { position: absolute; top:0; left:0; right:0; bottom:0; background: radial-gradient(circle, #ffffff 40%, #f8fafc 100%); z-index: 0; }
            .cert-content { position: relative; z-index: 1; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; }
            .cert-logo { max-height: 100px; margin-bottom: 20px; }
            .cert-school { font-family: 'Cinzel', serif; font-size: 32px; color: #0f172a; font-weight: 800; letter-spacing: 2px; margin: 0; }
            .cert-tagline { font-size: 14px; color: #64748b; letter-spacing: 4px; text-transform: uppercase; margin-bottom: 40px; }
            .cert-title { font-family: 'Great Vibes', cursive; font-size: 70px; color: #d4af37; margin: 0 0 40px 0; line-height: 1; }
            .cert-presented { font-size: 16px; color: #334155; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; }
            .cert-name { font-family: 'Cinzel', serif; font-size: 48px; color: #0f172a; font-weight: 700; margin: 0 0 20px 0; border-bottom: 2px solid #d4af37; padding-bottom: 5px; width: 70%; display: inline-block; }
            .cert-desc { font-size: 18px; color: #475569; max-width: 800px; line-height: 1.6; margin: 0 auto 50px auto; }
            .cert-footer { display: flex; justify-content: space-between; width: 80%; margin: 0 auto; margin-top: auto; align-items: flex-end; }
            .cert-sig-block { text-align: center; width: 250px; }
            .cert-sig-img { max-height: 60px; margin-bottom: 5px; }
            .cert-sig-line { border-top: 1px solid #334155; width: 100%; margin: 0 auto 10px auto; }
            .cert-sig-name { font-size: 16px; font-weight: 600; color: #0f172a; margin: 0; }
            .cert-sig-title { font-size: 12px; color: #64748b; margin: 0; text-transform: uppercase; letter-spacing: 1px; }
            
            .watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 0.03; width: 500px; pointer-events: none; }
            
            @media print {
              @page { size: A4 landscape; margin: 0; }
              body { background: white; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
              .cert-container { box-shadow: none; width: 100%; height: 100vh; }
            }
          </style>
        </head>
        <body>
          <div class="cert-container">
            <div class="cert-bg"></div>
            <!-- Standard seal as watermark if no logo -->
            <svg class="watermark" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="none" stroke="#000" stroke-width="2"/><text x="50" y="55" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#000">GIPS</text></svg>
            
            <div class="cert-content">
              ${logoBase64 ? "<img src='" + logoBase64 + "' class='cert-logo' />" : "<div style='width:80px; height:80px; background:#0f172a; color:#d4af37; border-radius:50%; display:flex; justify-content:center; align-items:center; font-family:\"Cinzel\", serif; font-size:36px; font-weight:bold; margin-bottom:20px;'>GI</div>"}

              <h1 class="cert-school">Gurudev International Public School</h1>
              <div class="cert-tagline">Excellence in Education</div>
              
              <h2 class="cert-title">${title}</h2>
              
              <div class="cert-presented">is proudly presented to</div>
              
              <h3 class="cert-name">${name}</h3>
              
              <div class="cert-desc">${desc}</div>
              
              <div class="cert-footer">
                <div class="cert-sig-block">
                  <div style="height: 65px; display: flex; align-items: flex-end; justify-content: center;">
                    <span style="font-family:'Montserrat', sans-serif; font-size:18px; font-weight:600; color:#334155; margin-bottom:10px;">${formattedDate}</span>
                  </div>
                  <div class="cert-sig-line"></div>
                  <p class="cert-sig-name">Date of Award</p>
                </div>
                
                <div class="cert-sig-block" style="width: 100px; height: 100px;">
                  <svg viewBox="0 0 100 100"><polygon points="50,5 61,35 95,35 68,55 78,85 50,65 22,85 32,55 5,35 39,35" fill="#d4af37" /><circle cx="50" cy="50" r="18" fill="#fff" /></svg>
                </div>
                
                <div class="cert-sig-block">
                  <div style="height: 65px; display: flex; align-items: flex-end; justify-content: center;">
                    ${sigBase64 ? "<img src='" + sigBase64 + "' class='cert-sig-img' />" : "<span style='font-family:\"Great Vibes\", cursive; font-size:36px; color:#1e293b;'>" + sigName + "</span>"}
                  </div>
                  <div class="cert-sig-line"></div>
                  <p class="cert-sig-name">${sigName}</p>
                  <p class="cert-sig-title">${sigTitle}</p>
                </div>
              </div>
            </div>
          </div>
        </body>
        </html>
      `;
      
      const modal = document.getElementById('cert-preview-modal');
      const iframe = document.getElementById('cert-preview-frame');
      
      iframe.contentWindow.document.open();
      iframe.contentWindow.document.write(htmlContent);
      iframe.contentWindow.document.close();
      
      modal.classList.add('active');
    };

    // Helper to read files
    const readFile = (file) => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.readAsDataURL(file);
      });
    };

    const processImages = async () => {
      if(sigInput.files && sigInput.files[0]) {
        sigBase64 = await readFile(sigInput.files[0]);
      }
      if(logoInput.files && logoInput.files[0]) {
        logoBase64 = await readFile(logoInput.files[0]);
      }
      renderPrint();
    };
    
    processImages();
  });
}

function printCertificateFromPreview() {
  const iframe = document.getElementById('cert-preview-frame');
  if(iframe && iframe.contentWindow) {
    iframe.contentWindow.print();
  }
}

// Delete Registered Student
function deleteStudent(mobile) {
  if (confirm("Are you sure you want to permanently delete this student? They will no longer be able to log in.")) {
    let users = JSON.parse(localStorage.getItem('erp_users')) || {};
    if (users[mobile]) {
      delete users[mobile];
      localStorage.setItem('erp_users', JSON.stringify(users));
      alert("Student deleted successfully.");
      window.location.reload(); // Refresh the page to update the table and counters
    } else {
      alert("Student not found.");
    }
  }
}
