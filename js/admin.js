/* admin.js - Superpower Admin Panel Logic (Light Theme & Sync Updates) */
var _fbReady = null;
try {
  _fbReady = Promise.all([
    import('./firebase-config.js'),
    import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
  ]).then(([c, fs]) => {
     // Auto-seed Admin Credentials into Firestore
     try {
       fs.setDoc(fs.doc(c.db, "admins", "admin"), {
          role: "admin",
          mobile: "gurudev@gmail.com",
          password: "Gurudev@2008",
          name: "Super Admin"
       }, { merge: true });
     } catch(err) { console.warn("Admin seed error:", err); }
     return { db: c.db, fs };
  }).catch(e => { 
     console.error('Firebase preload error:', e); 
     alert('Firebase Preload Error: ' + (e.message || String(e))); 
     return null; 
  });
} catch(e) { _fbReady = Promise.resolve(null); }
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

  // --- POPULATE CLASS-WISE STATS ---
  const classWiseStatsContainer = document.getElementById('class-wise-stats');

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
  loadQuickCallbacks();
  loadComplaints();
  
  // Load Galleries initially
  renderAchieversGalleryList();
  renderSchoolGalleryList();
  
  // Load News and Reviews
  renderNewsList();
  renderReviewsList();
loadAdminNotices();
  loadAdminLibrary();
  loadAdminResults();
  loadAdminCalendar();
  loadAdminDocuments();
  loadAdminTimetables();
  loadAdminAssignments();
});

// --- GLOBAL LOADER TOOL ---
function showLoader(title, desc, duration, callback) {
  const overlay = document.getElementById('admin-loader');
  const titleEl = document.getElementById('loader-title');
  const descEl = document.getElementById('loader-desc');
  
  if(overlay && titleEl && descEl) {
    titleEl.innerText = title;
    descEl.innerText = desc;
    overlay.classList.add('active');
    setTimeout(() => {
      overlay.classList.remove('active');
      if(callback) callback();
    }, duration);
  } else {
    // Elements missing — skip animation, just run callback
    if(callback) setTimeout(callback, 100);
  }
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

// --- IMAGE COMPRESSOR (Resizes & compresses for localStorage) ---
function compressImage(file, maxWidth, quality, callback) {
  const reader = new FileReader();
  reader.onload = function(e) {
    const img = new Image();
    img.onload = function() {
      const canvas = document.createElement('canvas');
      let w = img.width;
      let h = img.height;
      if(w > maxWidth) {
        h = Math.round(h * maxWidth / w);
        w = maxWidth;
      }
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, w, h);
      const compressed = canvas.toDataURL('image/jpeg', quality);
      callback(compressed);
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
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
  
  compressImage(file, 800, 0.7, function(compressedImage) {
    let gallery = JSON.parse(localStorage.getItem('admin_achievers_gallery') || '[]');
    
    gallery.unshift({ name, score, image: compressedImage });
    
    if(gallery.length > 10) gallery.pop();
    
    showLoader('Uploading Photo', 'Optimizing and syncing to the Homepage Slider...', 2000, () => {
      try {
        localStorage.setItem('admin_achievers_gallery', JSON.stringify(gallery));
        alert('Photo synced to the Homepage successfully! Go check the slider.');
      } catch(e) {
        alert('Storage full! Delete some old photos first.');
        console.warn('localStorage quota exceeded:', e);
      }
      document.getElementById('gallery-name').value = '';
      document.getElementById('gallery-score').value = '';
      fileInput.value = '';
      renderAchieversGalleryList();
    });
  });
}

// School Gallery Upload & Sync (FIREBASE)
function uploadSchoolGallery() {
  const fileInput = document.getElementById('school-gallery-photo');
  const descInput = document.getElementById('school-gallery-desc');
  if(!fileInput || fileInput.files.length === 0) return alert('Please select a photo to upload.');
  const desc = descInput ? descInput.value : '';
  const file = fileInput.files[0];
  const overlay = document.getElementById('admin-loader');
  if(overlay) { document.getElementById('loader-title').innerText = 'Uploading Photo'; document.getElementById('loader-desc').innerText = 'Uploading to cloud...'; overlay.classList.add('active'); }
  compressImage(file, 600, 0.5, function(compressedImage) {
    _fbReady.then(fb => {
      if(!fb) { alert('Firebase not ready. Try again.'); if(overlay) overlay.classList.remove('active'); return; }
      const { collection, addDoc } = fb.fs;
      addDoc(collection(fb.db, 'school_gallery'), { image: compressedImage, desc: desc, date: new Date().toLocaleDateString('en-GB'), timestamp: Date.now() }).then(() => {
        alert('Photo uploaded successfully!');
        fileInput.value = ''; if(descInput) descInput.value = '';
        if(document.getElementById('school-gallery-photo-name')) document.getElementById('school-gallery-photo-name').innerText = 'No file chosen';
        if(overlay) overlay.classList.remove('active');
        renderSchoolGalleryList();
      }).catch(err => { console.error('Upload error:', err); alert('Upload failed! Image may be too large.'); if(overlay) overlay.classList.remove('active'); });
    });
  });
}

// Render Achievers List
function renderAchieversGalleryList() {
  const listBody = document.getElementById('achievers-list');
  if(!listBody) return;
  
  let gallery = JSON.parse(localStorage.getItem('admin_achievers_gallery') || '[]');
  
  if(gallery.length === 0) {
    listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No achievers uploaded yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  gallery.forEach((item, index) => {
    listBody.innerHTML += `
      <tr>
        <td><img src="${item.image}" style="width:50px; height:50px; object-fit:cover; border-radius:8px;" alt="Achiever"></td>
        <td style="font-weight:600; color:var(--admin-heading);">${item.name}</td>
        <td style="color:var(--admin-muted);">${item.score}</td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteAchiever(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteAchiever(index) {
  if(!confirm("Are you sure you want to delete this achiever?")) return;
  let gallery = JSON.parse(localStorage.getItem('admin_achievers_gallery') || '[]');
  gallery.splice(index, 1);
  localStorage.setItem('admin_achievers_gallery', JSON.stringify(gallery));
  renderAchieversGalleryList();
}

// Render School Gallery List (FIREBASE)
function renderSchoolGalleryList() {
  const listBody = document.getElementById('school-gallery-list');
  if(!listBody) return;
  listBody.innerHTML = '<tr><td colspan="4" style="text-align:center;">Loading...</td></tr>';
  _fbReady.then(fb => {
    if(!fb) { listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:red;">Firebase not connected.</td></tr>'; return; }
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'school_gallery'), orderBy('timestamp', 'desc'))).then(snap => {
      if(snap.empty) { listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No photos uploaded yet.</td></tr>'; return; }
      listBody.innerHTML = '';
      snap.forEach(d => {
        const item = d.data(); const id = d.id;
        listBody.innerHTML += '<tr><td><img src="'+item.image+'" style="width:80px;height:50px;object-fit:cover;border-radius:8px;" alt="Gallery"></td><td style="font-weight:600;color:var(--admin-heading);">'+(item.desc||'N/A')+'</td><td style="color:var(--admin-muted);">'+(item.date||'N/A')+'</td><td><button class="btn-admin" style="background:#ef4444;padding:6px 12px;font-size:0.8rem;" onclick="deleteSchoolGallery(\''+id+'\')"><i class="fa-solid fa-trash"></i></button></td></tr>';
      });
    });
  });
}

function deleteSchoolGallery(id) {
  if(!confirm("Delete this photo?")) return;
  _fbReady.then(fb => {
    if(!fb) return;
    const { doc, deleteDoc } = fb.fs;
    deleteDoc(doc(fb.db, 'school_gallery', id)).then(() => {
      alert('Deleted!'); renderSchoolGalleryList();
    });
  });
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
        let status = 'Present'; // default if not marked
        if(st.attendanceRecords && st.attendanceRecords[dateObj]) {
          status = st.attendanceRecords[dateObj];
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
                <option value="Present" ${status === 'Present' ? 'selected' : ''}>Present</option>
                <option value="Absent" ${status === 'Absent' ? 'selected' : ''}>Absent</option>
                <option value="Holiday" ${status === 'Holiday' ? 'selected' : ''}>Holiday</option>
                <option value="Sunday" ${status === 'Sunday' ? 'selected' : ''}>Sunday</option>
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
        
        // Recalculate total attendance percentage
        let records = Object.values(users[mobile].attendanceRecords).filter(s => s === 'Present' || s === 'Absent');
        let presents = records.filter(s => s === 'Present').length;
        users[mobile].attendance = records.length > 0 ? Math.round((presents / records.length) * 100) : 0;
        
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
    if(typeof loadAdminNotices === 'function') loadAdminNotices();
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
    if(typeof loadAdminLibrary === 'function') loadAdminLibrary();
  });
}

// --- ADMISSIONS & CALLBACKS ---
function loadCallbacks() {
  const listBody = document.getElementById('callbacks-list');
  if(!listBody) return;
  
  listBody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px;">Loading from Firebase...</td></tr>';
  
  _fbReady.then(fb => {
    if(!fb) return;
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'callbacks'), orderBy('timestamp', 'desc'))).then(snapshot => {
      if(snapshot.empty) {
        listBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--admin-muted); padding:40px;">No online applications yet.</td></tr>';
        return;
      }
      listBody.innerHTML = '';
      snapshot.forEach(doc => {
        const cb = doc.data();
        listBody.innerHTML += `
          <tr>
            <td>${cb.date || 'N/A'}</td>
            <td><strong>${cb.name || 'N/A'}</strong></td>
            <td><a href="tel:${cb.phone}" style="color:var(--admin-accent); text-decoration:none;">${cb.phone}</a></td>
            <td><span class="status-badge status-active">${cb.position || cb.class || 'N/A'}</span></td>
            <td style="max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${cb.message || 'N/A'}">${cb.message || 'N/A'}</td>
            <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteLead('callbacks', '${doc.id}')"><i class="fa-solid fa-trash"></i></button></td>
          </tr>
        `;
      });
      updatePendingInquiriesCount();
    });
  });
}

function loadContactMessages() {
  const listBody = document.getElementById('contact-messages-list');
  if(!listBody) return;
  
  listBody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:20px;">Loading from Firebase...</td></tr>';
  
  _fbReady.then(fb => {
    if(!fb) return;
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'contact_messages'), orderBy('timestamp', 'desc'))).then(snapshot => {
      if(snapshot.empty) {
        listBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--admin-muted); padding:40px;">No contact inquiries yet.</td></tr>';
        return;
      }
      listBody.innerHTML = '';
      snapshot.forEach(doc => {
        const msg = doc.data();
        listBody.innerHTML += `
          <tr>
            <td>${msg.date || 'N/A'}</td>
            <td><strong>${msg.name || 'N/A'}</strong></td>
            <td><a href="tel:${msg.phone}" style="color:var(--admin-accent); text-decoration:none;">${msg.phone || 'N/A'}</a></td>
            <td>
              <a href="mailto:${msg.email}" style="color:var(--admin-muted); text-decoration:none; display:block; font-size:0.85rem;"><i class="fa-solid fa-envelope"></i> ${msg.email || 'N/A'}</a>
              <span style="font-weight:600; font-size:0.85rem;">${msg.subject || 'General'}</span>
            </td>
            <td style="max-width:250px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${msg.message || 'N/A'}">${msg.message || 'N/A'}</td>
            <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteLead('contact_messages', '${doc.id}')"><i class="fa-solid fa-trash"></i></button></td>
          </tr>
        `;
      });
      updatePendingInquiriesCount();
    });
  });
}

function loadComplaints() {
  const listBody = document.getElementById('complaints-list');
  if(!listBody) return;
  
  listBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px;">Loading from Firebase...</td></tr>';
  
  _fbReady.then(fb => {
    if(!fb) return;
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'complaints'), orderBy('timestamp', 'desc'))).then(snapshot => {
      if(snapshot.empty) {
        listBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted); padding:40px;">No complaints found.</td></tr>';
        return;
      }
      listBody.innerHTML = '';
      snapshot.forEach(doc => {
        const msg = doc.data();
        const isResolved = msg.status === 'Resolved';
        const statusHtml = isResolved 
          ? '<span style="color:#10b981; font-weight:700; font-size:0.85rem; padding:4px 8px; background:#dcfce7; border-radius:4px; display:inline-block; margin-right:5px;"><i class="fa-solid fa-check-double"></i> Resolved</span>'
          : `<button class="btn-admin" style="background:#10b981; padding:6px 12px; font-size:0.8rem; margin-right:5px;" onclick="resolveComplaint('${doc.id}')"><i class="fa-solid fa-check"></i> Mark Resolved</button>`;
          
        listBody.innerHTML += `
          <tr style="${isResolved ? 'opacity:0.6;' : ''}">
            <td>${msg.date || 'N/A'}</td>
            <td><strong>${msg.Name || 'Anonymous'}</strong></td>
            <td><a href="tel:${msg.Contact}" style="color:var(--admin-accent); text-decoration:none;">${msg.Contact || 'N/A'}</a></td>
            <td style="max-width:350px; white-space:pre-wrap; word-break:break-word;">${msg.Message || 'N/A'}</td>
            <td>
              ${statusHtml}
              <button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteLead('complaints', '${doc.id}')"><i class="fa-solid fa-trash"></i></button>
            </td>
          </tr>
        `;
      });
      updatePendingInquiriesCount();
    });
  });
}

window.resolveComplaint = function(docId) {
  _fbReady.then(fb => {
    if(!fb) return;
    fb.fs.updateDoc(fb.fs.doc(fb.db, 'complaints', docId), { status: 'Resolved' }).then(() => {
      loadComplaints();
      if (typeof showCustomAlert === 'function') {
        showCustomAlert("Resolved!", "The complaint has been marked as resolved.", "success");
      } else {
        alert("Complaint marked as resolved.");
      }
    });
  });
}

function loadQuickCallbacks() {
  const listBody = document.getElementById('quick-callbacks-list');
  if(!listBody) return;
  
  listBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px;">Loading from Firebase...</td></tr>';
  
  _fbReady.then(fb => {
    if(!fb) return;
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'quick_callbacks'), orderBy('timestamp', 'desc'))).then(snapshot => {
      if(snapshot.empty) {
        listBody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted); padding:40px;">No quick callbacks yet.</td></tr>';
        return;
      }
      listBody.innerHTML = '';
      snapshot.forEach(doc => {
        const lead = doc.data();
        listBody.innerHTML += `
          <tr>
            <td style="white-space:nowrap; color:var(--admin-muted); font-size:0.85rem;">${lead.date || 'N/A'}</td>
            <td>
              <div style="font-weight:600; color:var(--admin-accent);">${lead.name || 'N/A'}</div>
            </td>
            <td>
              <div style="font-size:0.85rem;"><i class="fa-solid fa-phone" style="color:var(--admin-muted)"></i> ${lead.phone || 'N/A'}</div>
              <div style="font-size:0.85rem;"><i class="fa-solid fa-envelope" style="color:var(--admin-muted)"></i> ${lead.email || 'N/A'}</div>
            </td>
            <td style="max-width: 250px; font-size:0.85rem;">
              <div style="margin-bottom:4px;"><strong>Addr:</strong> ${lead.address || 'N/A'}</div>
              <div style="color:var(--admin-muted);">${lead.message ? 'Msg: ' + lead.message : 'No message'}</div>
            </td>
            <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteLead('quick_callbacks', '${doc.id}')"><i class="fa-solid fa-trash"></i></button></td>
          </tr>
        `;
      });
      updatePendingInquiriesCount();
    });
  });
}

function deleteLead(collectionName, docId) {
  if(!confirm("Are you sure you want to delete this entry?")) return;
  
  _fbReady.then(fb => {
    if(!fb) return;
    fb.fs.deleteDoc(fb.fs.doc(fb.db, collectionName, docId)).then(() => {
      if (collectionName === 'callbacks') loadCallbacks();
      if (collectionName === 'contact_messages') loadContactMessages();
      if (collectionName === 'quick_callbacks') loadQuickCallbacks();
      if (collectionName === 'complaints') loadComplaints();
      updatePendingInquiriesCount();
    }).catch(e => {
      console.error(e);
      alert("Error deleting entry");
    });
  });
}

// --- EXAMINATION RESULTS ---
function addSubjectField() {
  const container = document.getElementById('dynamic-subjects-container');
  const div = document.createElement('div');
  div.className = 'subject-input-group';
  div.style.display = 'flex';
  div.style.gap = '10px';
  div.innerHTML = `
    <input type="text" class="admin-input subject-name" placeholder="Subject Name" style="flex:2;" />
    <input type="number" class="admin-input subject-marks" placeholder="Marks" style="flex:1;" />
    <button class="btn-admin" style="background:#ef4444; padding:0 10px;" onclick="this.parentElement.remove()"><i class="fa-solid fa-xmark"></i></button>
  `;
  container.appendChild(div);
}

function publishResult() {
  const roll = document.getElementById('res-roll').value.trim();
  const name = document.getElementById('res-name').value.trim();
  const cls = document.getElementById('res-class').value;
  
  if(!roll || !name) {
    return alert("Please enter Roll Number and Student Name.");
  }

  const subjectInputs = document.querySelectorAll('#dynamic-subjects-container .subject-input-group');
  let marks = {};
  let total = 0;
  let subjectCount = 0;
  let valid = true;
  
  subjectInputs.forEach(group => {
    const sName = group.querySelector('.subject-name').value.trim();
    const sMarks = Number(group.querySelector('.subject-marks').value);
    
    if (sName && !isNaN(sMarks)) {
      marks[sName] = sMarks;
      total += sMarks;
      subjectCount++;
    } else if (sName || group.querySelector('.subject-marks').value !== "") {
      valid = false; // partially filled field
    }
  });
  
  if (!valid || subjectCount === 0) {
    return alert("Please fill all provided subject names and marks correctly.");
  }

  showLoader('Publishing Result', 'Calculating percentage...', 1000, () => {
    const maxTotal = subjectCount * 100;
    const percent = ((total / maxTotal) * 100).toFixed(2);
    let status = percent >= 33 ? 'PASS' : 'FAIL';
    
    let results = JSON.parse(localStorage.getItem('erp_results')) || {};
    results[roll] = {
      roll: roll,
      name: name,
      class: cls,
      marks: marks,
      total: total,
      maxTotal: maxTotal,
      percentage: percent,
      status: status,
      date: new Date().toLocaleDateString('en-GB')
    };
    
    localStorage.setItem('erp_results', JSON.stringify(results));
    alert(`Result published! Total: ${total}/${maxTotal} (${percent}%). Status: ${status}`);
    if(typeof loadAdminResults === 'function') loadAdminResults();
    
    document.getElementById('res-roll').value = '';
    document.getElementById('res-name').value = '';
    
    // reset subjects to default 5 empty fields
    const container = document.getElementById('dynamic-subjects-container');
    container.innerHTML = `
      <div class="subject-input-group" style="display:flex; gap:10px;">
        <input type="text" class="admin-input subject-name" value="English" placeholder="Subject Name" style="flex:2;" />
        <input type="number" class="admin-input subject-marks" placeholder="Marks" style="flex:1;" />
      </div>
      <div class="subject-input-group" style="display:flex; gap:10px;">
        <input type="text" class="admin-input subject-name" value="Mathematics" placeholder="Subject Name" style="flex:2;" />
        <input type="number" class="admin-input subject-marks" placeholder="Marks" style="flex:1;" />
      </div>
      <div class="subject-input-group" style="display:flex; gap:10px;">
        <input type="text" class="admin-input subject-name" value="Science" placeholder="Subject Name" style="flex:2;" />
        <input type="number" class="admin-input subject-marks" placeholder="Marks" style="flex:1;" />
      </div>
      <div class="subject-input-group" style="display:flex; gap:10px;">
        <input type="text" class="admin-input subject-name" value="Social Studies" placeholder="Subject Name" style="flex:2;" />
        <input type="number" class="admin-input subject-marks" placeholder="Marks" style="flex:1;" />
      </div>
      <div class="subject-input-group" style="display:flex; gap:10px;">
        <input type="text" class="admin-input subject-name" value="Hindi" placeholder="Subject Name" style="flex:2;" />
        <input type="number" class="admin-input subject-marks" placeholder="Marks" style="flex:1;" />
      </div>
    `;
  });
}

function uploadBulkResults() {
  const fileInput = document.getElementById('bulk-result-file');
  if(!fileInput) return;
  const file = fileInput.files[0];
  if (!file) return alert("Please select an Excel or CSV file first.");

  const reader = new FileReader();
  reader.onload = function(e) {
    showLoader('Processing Data', 'Parsing uploaded file...', 500, () => {
      try {
        const data = e.target.result;
        // Parse with SheetJS
        const workbook = XLSX.read(data, {type: 'binary'});
        const firstSheet = workbook.SheetNames[0];
        const rows = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);
        
        if(rows.length === 0) return alert("The uploaded file is empty.");
        
        let results = JSON.parse(localStorage.getItem('erp_results')) || {};
        let addedCount = 0;
        
        rows.forEach(row => {
          // Find standard columns (case-insensitive)
          const getVal = (key) => {
            const foundKey = Object.keys(row).find(k => k.trim().toLowerCase() === key.toLowerCase());
            return foundKey ? row[foundKey] : null;
          };
          
          let roll = getVal('roll');
          let name = getVal('name');
          let cls = getVal('class');
          
          if(roll && name && cls) {
            let marks = {};
            let total = 0;
            let subjectCount = 0;
            
            Object.keys(row).forEach(k => {
              const lowerK = k.trim().toLowerCase();
              if(lowerK !== 'roll' && lowerK !== 'name' && lowerK !== 'class') {
                const sMarks = Number(row[k]);
                if(!isNaN(sMarks)) {
                  marks[k.trim()] = sMarks;
                  total += sMarks;
                  subjectCount++;
                }
              }
            });
            
            if (subjectCount > 0) {
              const maxTotal = subjectCount * 100;
              const percent = ((total / maxTotal) * 100).toFixed(2);
              const status = percent >= 33 ? 'PASS' : 'FAIL';
              
              results[String(roll).trim()] = {
                roll: String(roll).trim(),
                name: String(name).trim(),
                class: String(cls).trim(),
                marks: marks,
                total: total,
                maxTotal: maxTotal,
                percentage: percent,
                status: status,
                date: new Date().toLocaleDateString('en-GB')
              };
              addedCount++;
            }
          }
        });
        
        localStorage.setItem('erp_results', JSON.stringify(results));
        alert("Successfully uploaded " + addedCount + " student results!");
        if(typeof loadAdminResults === 'function') loadAdminResults();
        fileInput.value = '';
      } catch (err) {
        console.error(err);
        alert("Error parsing file. Please ensure it is a valid Excel/CSV file with correct headers.");
      }
    });
  };
  
  reader.onerror = function() {
    alert("Error reading the file.");
  };
  
  reader.readAsBinaryString(file);
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
    
    alert("SMS API Triggered Successfully!\\n\\nMessage queued for " + targetStudents.length + " recipients.\\nTarget: " + (target === 'all' ? 'All Students' : 'Class ' + target));
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
      opt.textContent = u.name + " (ID: " + u.id + ")";
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

// Edit Registered Student
function editStudent(mobile) {
  let users = JSON.parse(localStorage.getItem('erp_users')) || {};
  let st = users[mobile];
  if(st) {
    let newName = prompt("Edit Student Name:", st.name);
    if(newName === null) return;
    let newClass = prompt("Edit Class:", st.class);
    if(newClass === null) return;
    let newPassword = prompt("Edit Password:", st.password);
    if(newPassword === null) return;
    
    st.name = newName.trim() || st.name;
    st.class = newClass.trim() || st.class;
    st.password = newPassword.trim() || st.password;
    
    users[mobile] = st;
    localStorage.setItem('erp_users', JSON.stringify(users));
    alert("Student details updated successfully!");
    window.location.reload();
  }
}

// --- SCHOOL CALENDAR ---
let adminCalDate = new Date();

function loadAdminCalendar() {
  const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const year = adminCalDate.getFullYear();
  const month = adminCalDate.getMonth();
  
  document.getElementById('admin-calendar-title').innerText = `${monthNames[month]} ${year}`;
  
  const grid = document.getElementById('admin-calendar-grid');
  if(!grid) return;
  grid.innerHTML = '';
  
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  let calendarData = JSON.parse(localStorage.getItem('erp_calendar')) || {};
  
  // Empty blocks for days before start of month
  for (let i = 0; i < firstDay; i++) {
    grid.innerHTML += `<div class="cal-day cal-empty"></div>`;
  }
  
  // Days of month
  for (let d = 1; d <= daysInMonth; d++) {
    let dateStr = `${year}-${String(month+1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    let data = calendarData[dateStr];
    let type = data ? (typeof data === 'string' ? data : data.type) : '';
    let title = data && data.title ? data.title : '';
    
    let cls = 'cal-day';
    if(type === 'holiday') cls += ' cal-holiday';
    if(type === 'event') cls += ' cal-event';
    if(type === 'exam') cls += ' cal-exam';
    
    grid.innerHTML += `<div class="${cls}" title="${title}" onclick="toggleCalDay('${dateStr}')">${d}</div>`;
  }
}

function changeAdminMonth(step) {
  adminCalDate.setMonth(adminCalDate.getMonth() + step);
  loadAdminCalendar();
}

let currentCalDate = '';

function toggleCalDay(dateStr) {
  currentCalDate = dateStr;
  let calendarData = JSON.parse(localStorage.getItem('erp_calendar')) || {};
  let current = calendarData[dateStr];
  
  document.getElementById('cal-modal-date').innerText = dateStr;
  
  if (current) {
    document.getElementById('cal-modal-type').value = current.type;
    document.getElementById('cal-modal-title').value = current.title || '';
    document.getElementById('cal-title-group').style.display = 'block';
  } else {
    document.getElementById('cal-modal-type').value = '';
    document.getElementById('cal-modal-title').value = '';
    document.getElementById('cal-title-group').style.display = 'none';
  }
  
  document.getElementById('calendar-modal').classList.add('active');
}

window.saveCalendarEvent = function() {
  let type = document.getElementById('cal-modal-type').value;
  let title = document.getElementById('cal-modal-title').value.trim();
  let calendarData = JSON.parse(localStorage.getItem('erp_calendar')) || {};
  
  if (!type) {
    delete calendarData[currentCalDate];
  } else {
    calendarData[currentCalDate] = { type: type, title: title };
  }
  
  localStorage.setItem('erp_calendar', JSON.stringify(calendarData));
  document.getElementById('calendar-modal').classList.remove('active');
  loadAdminCalendar();
}

// --- STUDENT DOCUMENTS ---
function loadAdminDocuments() {
  const users = JSON.parse(localStorage.getItem('erp_users')) || {};
  const students = Object.values(users).filter(u => u.role === 'student');
  renderAdminDocumentsTable(students);
}

function filterAdminDocuments() {
  const classFilter = document.getElementById('doc-class-filter').value;
  const nameQuery = document.getElementById('doc-name-search').value.toLowerCase();
  
  const users = JSON.parse(localStorage.getItem('erp_users')) || {};
  let students = Object.values(users).filter(u => u.role === 'student');
  
  if (classFilter) students = students.filter(s => s.class === classFilter);
  if (nameQuery) students = students.filter(s => s.name && s.name.toLowerCase().includes(nameQuery));
  
  renderAdminDocumentsTable(students);
}

function renderAdminDocumentsTable(students) {
  const list = document.getElementById('admin-documents-list');
  if(!list) return;
  list.innerHTML = '';
  
  if(students.length === 0) {
    list.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted); padding: 40px 0;">No students match your filter.</td></tr>';
    return;
  }
  
  students.forEach(st => {
    let docs = st.documents || {};
    let uploadedCount = Object.keys(docs).length;
    let badgeColor = uploadedCount === 8 ? '#10b981' : (uploadedCount > 0 ? '#f59e0b' : '#ef4444');
    
    list.innerHTML += `
      <tr>
        <td class="student-cell">
          <img src="${st.photoURL || 'assets/images/default-avatar.png'}" alt="Photo">
          <div><h5>${st.name}</h5><p>${st.mobile}</p></div>
        </td>
        <td>
          <strong style="color:var(--admin-accent); font-family:monospace;">${st.studentId || 'N/A'}</strong><br>
          <span style="font-size:0.85rem; color:var(--admin-muted);">Class ${st.class || 'N/A'}</span>
        </td>
        <td>
          <div style="display:inline-block; padding:4px 10px; border-radius:12px; background:${badgeColor}20; color:${badgeColor}; font-size:0.8rem; font-weight:700;">
            ${uploadedCount} / 8 Uploaded
          </div>
        </td>
        <td>
          <button class="btn-admin-outline" style="padding:6px 12px; font-size:0.75rem;" onclick="viewStudentDocs('${st.mobile}')">
            <i class="fa-regular fa-folder-open"></i> View Vault
          </button>
        </td>
      </tr>
    `;
  });
}

window.viewStudentDocs = function(mobile) {
  const users = JSON.parse(localStorage.getItem('erp_users')) || {};
  const st = users[mobile];
  if(!st) return;
  
  window.currentDocMobile = mobile; // Save for download all
  
  document.getElementById('doc-modal-student-name').innerText = `${st.name} (ID: ${st.studentId || 'N/A'})`;
  
  const docTypes = [
    "Aadhaar Card", "Marksheet (10th/Last Class)", "Samagra ID", 
    "Domicile Certificate (मूल निवासी)", "Income Certificate (आय प्रमाण पत्र)", 
    "Caste Certificate (जाति प्रमाण पत्र)", "Transfer Certificate (TC)", "Passport Size Photo"
  ];
  
  const grid = document.getElementById('doc-modal-grid');
  grid.innerHTML = '';
  
  let docs = st.documents || {};
  
  docTypes.forEach(docName => {
    let docData = docs[docName];
    if (docData) {
      grid.innerHTML += `
        <div style="border:1px solid var(--admin-border); border-radius:12px; padding:12px; background:#f8fafc; text-align:center;">
          <h4 style="font-size:0.85rem; color:var(--admin-heading); margin-bottom:10px;">${docName}</h4>
          <a href="${docData}" target="_blank" title="Click to view full screen">
            <img src="${docData}" style="width:100%; height:150px; object-fit:contain; border-radius:8px; border:1px solid #e2e8f0; background:white; cursor:zoom-in;">
          </a>
        </div>
      `;
    } else {
      grid.innerHTML += `
        <div style="border:1px dashed #cbd5e1; border-radius:12px; padding:12px; background:#f1f5f9; display:flex; flex-direction:column; align-items:center; justify-content:center; height:200px;">
          <i class="fa-solid fa-file-circle-xmark" style="font-size:2rem; color:#94a3b8; margin-bottom:10px;"></i>
          <h4 style="font-size:0.85rem; color:#64748b; margin:0; text-align:center;">${docName}</h4>
          <span style="font-size:0.75rem; color:#ef4444; font-weight:700; margin-top:5px;">Not Uploaded</span>
        </div>
      `;
    }
  });
  
  document.getElementById('doc-viewer-modal').classList.add('active');
}

window.downloadAllStudentDocs = function() {
  if (!window.currentDocMobile) return;
  const users = JSON.parse(localStorage.getItem('erp_users')) || {};
  const st = users[window.currentDocMobile];
  if (!st || !st.documents) return alert("No documents found for this student.");

  let docs = st.documents;
  let downloadedCount = 0;

  for (let docName in docs) {
    if (docs.hasOwnProperty(docName) && docs[docName]) {
      const link = document.createElement("a");
      link.href = docs[docName];
      link.download = `${st.name}_${docName}.jpg`.replace(/[^a-zA-Z0-9_\.]/g, '_');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      downloadedCount++;
    }
  }

  if (downloadedCount > 0) {
    showLoader("Downloading...", "Your files are downloading. Please check your downloads folder.", 1500, null);
  } else {
    alert("No documents are uploaded yet.");
  }
}

// --- NEWS & EVENTS ---
function publishNews() {
  const category = document.getElementById('news-category').value;
  const title = document.getElementById('news-title').value;
  const excerpt = document.getElementById('news-excerpt').value;
  const fileInput = document.getElementById('news-photo');
  
  if(!title || !excerpt) return alert("Please fill all fields.");

  let file = fileInput ? fileInput.files[0] : null;
  if(!file) {
    saveNews({ category, title, excerpt, image: null });
    return;
  }
  
  compressImage(file, 800, 0.7, function(compressedImage) {
    saveNews({ category, title, excerpt, image: compressedImage });
  });
}

function saveNews(newsItem) {
  showLoader('Publishing News', 'Syncing to website...', 1000, () => {
    let news = JSON.parse(localStorage.getItem('admin_news_events')) || [];
    newsItem.id = Date.now();
    newsItem.date = new Date().toLocaleDateString('en-GB');
    news.unshift(newsItem);
    try {
      localStorage.setItem('admin_news_events', JSON.stringify(news));
    } catch(e) {
      // If image is too large for localStorage, save without image
      console.warn('Image too large, saving without image:', e);
      newsItem.image = null;
      localStorage.setItem('admin_news_events', JSON.stringify(news));
    }
    alert('News published successfully!');
    document.getElementById('news-title').value = '';
    document.getElementById('news-excerpt').value = '';
    if(document.getElementById('news-photo')) document.getElementById('news-photo').value = '';
    renderNewsList();
  });
}

function renderNewsList() {
  const list = document.getElementById('news-list');
  if(!list) return;
  
  let news = JSON.parse(localStorage.getItem('admin_news_events')) || [];
  if(news.length === 0) {
    list.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted);">No news published yet.</td></tr>';
    return;
  }
  
  list.innerHTML = '';
  news.forEach((n, idx) => {
    list.innerHTML += `
      <tr>
        <td>${n.date}</td>
        <td><span style="background:var(--admin-primary); color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem;">${n.category}</span></td>
        <td style="font-weight:600;">${n.title}</td>
        <td style="color:var(--admin-muted); max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${n.excerpt}</td>
        <td><button class="btn-admin" style="background:var(--admin-danger); padding:4px 8px; font-size:0.8rem;" onclick="deleteNews(${idx})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteNews(idx) {
  if(!confirm("Delete this news item?")) return;
  let news = JSON.parse(localStorage.getItem('admin_news_events')) || [];
  news.splice(idx, 1);
  localStorage.setItem('admin_news_events', JSON.stringify(news));
  renderNewsList();
}

// --- STUDENT REVIEWS ---
function renderReviewsList() {
  const pendingList = document.getElementById('pending-reviews-list');
  const approvedList = document.getElementById('approved-reviews-list');
  if(!pendingList || !approvedList) return;
  
  pendingList.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px;">Loading from Firebase...</td></tr>';
  approvedList.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:20px;">Loading from Firebase...</td></tr>';
  
  _fbReady.then(fb => {
    if(!fb) return;
    const { collection, getDocs, query, orderBy } = fb.fs;
    getDocs(query(collection(fb.db, 'reviews'), orderBy('timestamp', 'desc'))).then(snapshot => {
      let pending = [];
      let approved = [];
      
      snapshot.forEach(doc => {
        let r = doc.data();
        r.id = doc.id;
        if (r.status === 'pending') pending.push(r);
        else approved.push(r);
      });
      
      if(pending.length === 0) {
        pendingList.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted);">No pending reviews.</td></tr>';
      } else {
        pendingList.innerHTML = '';
        pending.forEach(r => {
          pendingList.innerHTML += `
            <tr>
              <td>${r.date || 'N/A'}</td>
              <td><strong>${r.name || 'Anonymous'}</strong><br><small style="color:var(--admin-muted);">${r.role || 'Student'}</small></td>
              <td style="color:gold;">${'★'.repeat(Number(r.rating || 5))}</td>
              <td>${r.text || 'N/A'}</td>
              <td>
                <button class="btn-admin" style="background:#16a34a; padding:4px 8px; font-size:0.8rem; margin-right:5px;" onclick="approveReview('${r.id}')"><i class="fa-solid fa-check"></i></button>
                <button class="btn-admin" style="background:var(--admin-danger); padding:4px 8px; font-size:0.8rem;" onclick="deleteReview('${r.id}')"><i class="fa-solid fa-trash"></i></button>
              </td>
            </tr>
          `;
        });
      }
      
      if(approved.length === 0) {
        approvedList.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted);">No approved reviews.</td></tr>';
      } else {
        approvedList.innerHTML = '';
        approved.forEach(r => {
          approvedList.innerHTML += `
            <tr>
              <td>${r.date || 'N/A'}</td>
              <td><strong>${r.name || 'Anonymous'}</strong><br><small style="color:var(--admin-muted);">${r.role || 'Student'}</small></td>
              <td style="color:gold;">${'★'.repeat(Number(r.rating || 5))}</td>
              <td>${r.text || 'N/A'}</td>
              <td>
                <button class="btn-admin" style="background:var(--admin-danger); padding:4px 8px; font-size:0.8rem;" onclick="deleteReview('${r.id}')"><i class="fa-solid fa-trash"></i></button>
              </td>
            </tr>
          `;
        });
      }
    });
  });
}

function approveReview(id) {
  _fbReady.then(fb => {
    if(!fb) return;
    fb.fs.updateDoc(fb.fs.doc(fb.db, 'reviews', id), { status: 'approved' }).then(() => {
      renderReviewsList();
    });
  });
}

function deleteReview(id) {
  if(!confirm("Are you sure you want to delete this review?")) return;
  _fbReady.then(fb => {
    if(!fb) return;
    fb.fs.deleteDoc(fb.fs.doc(fb.db, 'reviews', id)).then(() => {
      renderReviewsList();
    });
  });
}

// --- NOTICES MANAGEMENT ---
function loadAdminNotices() {
  const list = document.getElementById('admin-notices-list');
  if(!list) return;
  
  let notices = JSON.parse(localStorage.getItem('erp_notices')) || [];
  if(notices.length === 0) {
    list.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No notices published yet.</td></tr>';
    return;
  }
  
  list.innerHTML = '';
  notices.forEach((n, idx) => {
    list.innerHTML += `
      <tr>
        <td>${n.date}</td>
        <td style="font-weight:600;">${n.title}</td>
        <td style="color:var(--admin-muted); max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${n.body}</td>
        <td><button class="btn-admin" style="background:var(--admin-danger); padding:4px 8px; font-size:0.8rem;" onclick="deleteNotice(${idx})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteNotice(idx) {
  if(!confirm("Delete this notice?")) return;
  let notices = JSON.parse(localStorage.getItem('erp_notices')) || [];
  notices.splice(idx, 1);
  localStorage.setItem('erp_notices', JSON.stringify(notices));
  loadAdminNotices();
}

// --- E-LIBRARY MANAGEMENT ---
function loadAdminLibrary() {
  const list = document.getElementById('admin-library-list');
  if(!list) return;
  
  let library = JSON.parse(localStorage.getItem('erp_library')) || [];
  if(library.length === 0) {
    list.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--admin-muted);">No books in E-Library yet.</td></tr>';
    return;
  }
  
  list.innerHTML = '';
  library.forEach((book, idx) => {
    list.innerHTML += `
      <tr>
        <td>${book.date}</td>
        <td><span style="background:var(--admin-primary); color:white; padding:2px 8px; border-radius:12px; font-size:0.75rem;">${book.subject}</span></td>
        <td style="font-weight:600;">${book.name}</td>
        <td><a href="${book.link}" target="_blank" style="color:var(--admin-accent); text-decoration:underline;">View Link</a></td>
        <td><button class="btn-admin" style="background:var(--admin-danger); padding:4px 8px; font-size:0.8rem;" onclick="deleteLibrary(${idx})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteLibrary(idx) {
  if(!confirm("Delete this book from E-Library?")) return;
  let library = JSON.parse(localStorage.getItem('erp_library')) || [];
  library.splice(idx, 1);
  localStorage.setItem('erp_library', JSON.stringify(library));
  loadAdminLibrary();
}

// --- RESULTS MANAGEMENT ---
function loadAdminResults() {
  const list = document.getElementById('admin-results-list');
  if(!list) return;
  
  let results = JSON.parse(localStorage.getItem('erp_results')) || {};
  let rolls = Object.keys(results);
  
  if(rolls.length === 0) {
    list.innerHTML = '<tr><td colspan="7" style="text-align:center; color:var(--admin-muted);">No results found.</td></tr>';
    return;
  }
  
  list.innerHTML = '';
  rolls.forEach(roll => {
    let r = results[roll];
    let badgeClass = r.status === 'PASS' ? 'status-active' : 'status-inactive';
    list.innerHTML += `
      <tr>
        <td style="font-weight:bold;">${r.roll}</td>
        <td>${r.name}</td>
        <td>${r.class}</td>
        <td>${r.total} / ${r.maxTotal}</td>
        <td>${r.percentage}%</td>
        <td><span class="status-badge ${badgeClass}">${r.status}</span></td>
        <td><button class="btn-admin" style="background:var(--admin-danger); padding:4px 8px; font-size:0.8rem;" onclick="deleteResult('${r.roll}')"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteResult(roll) {
  if(!confirm("Are you sure you want to delete the result for Roll No: " + roll + "?")) return;
  let results = JSON.parse(localStorage.getItem('erp_results')) || {};
  if(results[roll]) {
    delete results[roll];
    localStorage.setItem('erp_results', JSON.stringify(results));
    loadAdminResults();
  }
}


// --- TIMETABLE & ASSIGNMENTS ---
function uploadTimetable() {
  const classVal = document.getElementById('tt-class').value;
  const fileInput = document.getElementById('tt-file');
  
  if(!classVal || fileInput.files.length === 0) {
    return alert('Please select a class and upload a file.');
  }

  const file = fileInput.files[0];
  
  // Basic simulation of upload: converting small files to base64 for localstorage demo
  // In production, upload to Firebase Storage and save URL.
  const reader = new FileReader();
  reader.onload = function(e) {
    let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
    // Remove old timetable for this class if exists
    timetables = timetables.filter(t => t.class !== classVal);
    
    timetables.unshift({
      class: classVal,
      fileData: e.target.result,
      fileName: file.name,
      date: new Date().toLocaleDateString('en-GB')
    });
    
    showLoader('Uploading Timetable', 'Syncing to Student Portal...', 1500, () => {
      try {
        localStorage.setItem('admin_timetables', JSON.stringify(timetables));
        alert('Timetable uploaded successfully!');
        fileInput.value = '';
        loadAdminTimetables();
      } catch(e) {
        alert('File is too large for local storage! Use a smaller file.');
      }
    });
  };
  reader.readAsDataURL(file);
}

function loadAdminTimetables() {
  const listBody = document.getElementById('admin-timetables-list');
  if(!listBody) return;
  
  let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
  
  if(timetables.length === 0) {
    listBody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:var(--admin-muted);">No timetables uploaded yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  timetables.forEach((item, index) => {
    listBody.innerHTML += `
      <tr>
        <td>${item.date}</td>
        <td style="font-weight:600;">Class ${item.class}</td>
        <td><a href="${item.fileData}" target="_blank" style="color:var(--admin-primary);"><i class="fa-solid fa-file"></i> ${item.fileName}</a></td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteTimetable(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteTimetable(index) {
  if(!confirm("Are you sure you want to delete this timetable?")) return;
  let timetables = JSON.parse(localStorage.getItem('admin_timetables') || '[]');
  timetables.splice(index, 1);
  localStorage.setItem('admin_timetables', JSON.stringify(timetables));
  loadAdminTimetables();
}

function publishAssignment() {
  const classVal = document.getElementById('assign-class').value;
  const subject = document.getElementById('assign-subject').value;
  const title = document.getElementById('assign-title').value;
  const deadline = document.getElementById('assign-deadline').value;
  const fileInput = document.getElementById('assign-file');
  
  if(!classVal || !subject || !title || !deadline) {
    return alert('Please fill all assignment fields.');
  }

  const saveAssignmentData = (fileData = null, fileName = null) => {
    showLoader('Publishing Assignment', 'Notifying Class ' + classVal + '...', 1000, () => {
      let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
      
      assignments.unshift({
        class: classVal,
        subject: subject,
        title: title,
        deadline: deadline,
        dateGiven: new Date().toLocaleDateString('en-GB'),
        fileData: fileData,
        fileName: fileName
      });
      
      try {
        localStorage.setItem('admin_assignments', JSON.stringify(assignments));
        alert('Assignment published successfully!');
      } catch (e) {
        alert('File is too large! Please upload a smaller image.');
        return;
      }
      
      document.getElementById('assign-subject').value = '';
      document.getElementById('assign-title').value = '';
      document.getElementById('assign-deadline').value = '';
      if(fileInput) fileInput.value = '';
      
      loadAdminAssignments();
    });
  };

  if(fileInput && fileInput.files.length > 0) {
    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = function(e) {
      saveAssignmentData(e.target.result, file.name);
    };
    reader.readAsDataURL(file);
  } else {
    saveAssignmentData();
  }
}

function loadAdminAssignments() {
  const listBody = document.getElementById('admin-assignments-list');
  if(!listBody) return;
  
  let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
  
  if(assignments.length === 0) {
    listBody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:var(--admin-muted);">No assignments published yet.</td></tr>';
    return;
  }
  
  listBody.innerHTML = '';
  assignments.forEach((item, index) => {
    let attachmentHTML = item.fileData ? `<a href="${item.fileData}" target="_blank" style="color:var(--admin-primary); font-size:0.85rem;"><i class="fa-solid fa-paperclip"></i> Attachment</a>` : '';
    listBody.innerHTML += `
      <tr>
        <td>${item.dateGiven}</td>
        <td style="font-weight:600;">Class ${item.class}</td>
        <td>${item.subject}</td>
        <td>
          <div style="font-weight:600;">${item.title}</div>
          ${attachmentHTML}
        </td>
        <td style="color:#ef4444; font-weight:600;">${item.deadline}</td>
        <td><button class="btn-admin" style="background:#ef4444; padding:6px 12px; font-size:0.8rem;" onclick="deleteAssignment(${index})"><i class="fa-solid fa-trash"></i></button></td>
      </tr>
    `;
  });
}

function deleteAssignment(index) {
  if(!confirm("Are you sure you want to delete this assignment?")) return;
  let assignments = JSON.parse(localStorage.getItem('admin_assignments') || '[]');
  assignments.splice(index, 1);
  localStorage.setItem('admin_assignments', JSON.stringify(assignments));
  loadAdminAssignments();
}
