// --- LOCAL STORAGE DATABASE ENGINE (STUDENT DASHBOARD) ---

// 1. Session Management
const currentUserData = localStorage.getItem('erp_current_user');
let user = null;

if (!currentUserData) {
  window.location.href = "student-portal.html";
} else {
  user = JSON.parse(currentUserData);
  
  // Populate Profile Banner
  document.getElementById('topProfileName').textContent = user.name || 'Student';
  document.getElementById('topProfileMobile').textContent = user.mobile || '---';
  document.getElementById('topProfileClass').textContent = user.class ? `Class ${user.class}` : 'N/A';
  document.getElementById('topProfileId').textContent = user.studentId || 'Pending';
  
  if (user.photoURL) {
    document.getElementById('topProfileImg').src = user.photoURL;
  }
}

// --- PROFILE PHOTO UPLOAD (CIRCULAR CROP) ---
window.updateProfilePhoto = function(input) {
  if (input.files && input.files[0]) {
    const file = input.files[0];
    
    // Change icon temporarily
    const label = input.parentElement;
    const icon = label.querySelector('i');
    if (icon) icon.className = 'fa-solid fa-spinner fa-spin';
    
    const reader = new FileReader();
    reader.onload = function(e) {
      const img = new Image();
      img.onload = function() {
        const size = Math.min(img.width, img.height);
        
        // Final image size (max 300px to save storage)
        const targetSize = Math.min(size, 300);
        
        const canvas = document.createElement('canvas');
        canvas.width = targetSize;
        canvas.height = targetSize;
        const ctx = canvas.getContext('2d');
        
        // Circular clip
        ctx.beginPath();
        ctx.arc(targetSize/2, targetSize/2, targetSize/2, 0, Math.PI*2, true);
        ctx.closePath();
        ctx.clip();
        
        // Draw image centered and cropped
        const startX = (img.width - size) / 2;
        const startY = (img.height - size) / 2;
        ctx.drawImage(img, startX, startY, size, size, 0, 0, targetSize, targetSize);
        
        // Save as PNG to maintain transparency of the corners
        const compressedData = canvas.toDataURL('image/png');
        
        try {
          let allUsers = JSON.parse(localStorage.getItem('erp_users')) || {};
          if (allUsers[user.mobile]) {
            allUsers[user.mobile].photoURL = compressedData;
            localStorage.setItem('erp_users', JSON.stringify(allUsers));
            
            user.photoURL = compressedData;
            localStorage.setItem('erp_current_user', JSON.stringify(user));
            
            document.getElementById('topProfileImg').src = compressedData;
          }
        } catch(err) {
          console.error(err);
          alert("Storage full! Please delete some old documents first.");
        }
        
        if (icon) icon.className = 'fa-solid fa-camera';
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// 2. Logout Logic
const btnLogout = document.getElementById('btnLogout');
if (btnLogout) {
  btnLogout.addEventListener('click', () => {
    localStorage.removeItem('erp_current_user');
    window.location.href = "student-portal.html";
  });
}

// 3. Modals & A-Z Feature Logic
const modalOverlay = document.getElementById('erpModalOverlay');
const modalClose = document.getElementById('modalClose');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');

function openModal(title, contentHTML) {
  modalTitle.textContent = title;
  modalBody.innerHTML = contentHTML;
  modalOverlay.classList.add('active');
}

modalClose.addEventListener('click', () => {
  modalOverlay.classList.remove('active');
});
modalOverlay.addEventListener('click', (e) => {
  if(e.target === modalOverlay) modalOverlay.classList.remove('active');
});

// Helper for beautiful empty states
const emptyState = (iconClass, text, subtext) => `
  <div style="text-align:center; padding: 40px 20px;">
    <div style="font-size:3rem; color:#cbd5e1; margin-bottom:16px;"><i class="${iconClass}"></i></div>
    <h4 style="color:#475569; margin:0 0 8px 0; font-size:1.1rem;">${text}</h4>
    <p style="color:#94a3b8; font-size:0.9rem; margin:0;">${subtext}</p>
  </div>
`;

const modules = [
  {
    selector: '.feature-card:nth-child(1)',
    title: 'Certificates & Badges',
    render: () => {
      let html = '';
      if(user.badges && user.badges.length > 0) {
        user.badges.forEach(b => {
          html += `<div class="modal-list-item" style="padding:15px; border:1px solid #e2e8f0; border-radius:8px; margin-bottom:10px; display:flex; align-items:center; gap:12px;"><div style="width:40px;height:40px;background:#3b82f6;color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;"><i class="fa-solid fa-medal"></i></div><div style="font-weight:600; font-size:1.05rem;">${b}</div></div>`;
        });
      }
      
      if(user.certificates && user.certificates.length > 0) {
        user.certificates.forEach(c => {
          html += `<div class="modal-list-item" style="padding:15px; border:1px solid #e2e8f0; border-radius:8px; margin-bottom:10px; display:flex; align-items:center; gap:12px; background:#f8fafc;"><div style="width:40px;height:40px;background:var(--accent);color:white;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.2rem;"><i class="fa-solid fa-award"></i></div><div><div style="font-weight:600; font-size:1.05rem;">${c.type}</div><div style="font-size:0.8rem; color:#64748b;">Issued on ${c.date}</div></div></div>`;
        });
      }

      if(html === '') {
        return emptyState('fa-solid fa-award', 'No Certificates Yet', 'Keep up the good work to earn your first achievement certificate!');
      }
      return html;
    }
  },
  {
    selector: '.feature-card:nth-child(2)',
    title: 'School Calendar',
    render: () => {
      if(!window.studentCalDate) window.studentCalDate = new Date();
      
      window.renderStudentCalendar = function() {
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const year = window.studentCalDate.getFullYear();
        const month = window.studentCalDate.getMonth();
        
        const firstDay = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        let calendarData = JSON.parse(localStorage.getItem('erp_calendar')) || {};
        
        let gridHTML = '';
        for (let i = 0; i < firstDay; i++) {
          gridHTML += `<div class="cal-day cal-empty"></div>`;
        }
        
        for (let d = 1; d <= daysInMonth; d++) {
          let dateStr = `${year}-${String(month+1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
          let data = calendarData[dateStr];
          let type = data ? (typeof data === 'string' ? data : data.type) : '';
          let title = data && data.title ? data.title : '';
          
          let cls = 'cal-day';
          if(type === 'holiday') cls += ' cal-holiday';
          if(type === 'event') cls += ' cal-event';
          if(type === 'exam') cls += ' cal-exam';
          
          gridHTML += `<div class="${cls}" title="${title}" style="cursor:default;">${d}</div>`;
        }
        
        return `
          <div style="max-width: 600px; margin: 0 auto;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
              <button class="btn btn-secondary" style="padding:8px 12px;" onclick="window.changeStudentMonth(-1)"><i class="fa-solid fa-chevron-left"></i></button>
              <h3 style="margin:0; font-family:var(--font-primary); font-size:1.2rem; color:var(--text-color);">${monthNames[month]} ${year}</h3>
              <button class="btn btn-secondary" style="padding:8px 12px;" onclick="window.changeStudentMonth(1)"><i class="fa-solid fa-chevron-right"></i></button>
            </div>
            
            <div style="display:grid; grid-template-columns:repeat(7, 1fr); text-align:center; font-weight:bold; color:#64748b; margin-bottom:10px;">
              <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
            </div>
            
            <div style="display:grid; grid-template-columns:repeat(7, 1fr); gap:10px;">
              ${gridHTML}
            </div>
            
            <div style="display:flex; justify-content:center; gap:20px; margin-top:24px; font-size:0.9rem; font-weight:600; color:#475569;">
              <div style="display:flex; align-items:center; gap:5px;"><div style="width:12px; height:12px; border-radius:3px; background:#ef4444;"></div> Holiday</div>
              <div style="display:flex; align-items:center; gap:5px;"><div style="width:12px; height:12px; border-radius:3px; background:#22c55e;"></div> Event</div>
              <div style="display:flex; align-items:center; gap:5px;"><div style="width:12px; height:12px; border-radius:3px; background:#3b82f6;"></div> Exam</div>
            </div>
          </div>
        `;
      };

      window.changeStudentMonth = function(step) {
        window.studentCalDate.setMonth(window.studentCalDate.getMonth() + step);
        document.getElementById('modalBody').innerHTML = window.renderStudentCalendar();
      };
      
      return window.renderStudentCalendar();
    }
  },
  {
    selector: '.feature-card:nth-child(3)',
    title: 'My Attendance',
    render: () => {
      // Fetch fresh data from local storage
      let allUsers = JSON.parse(localStorage.getItem('erp_users')) || {};
      let freshUser = allUsers[user.mobile] || user;
      
      let records = freshUser.attendanceRecords || {};
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
          
          if(status !== 'Holiday' && status !== 'Sunday') {
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
      
      let percentage = totalWorkingDays > 0 ? Math.round((presents / totalWorkingDays) * 100) : 0;
      
      return `
        <div style="text-align:center; padding: 20px 0;">
          <div style="font-size: 3.5rem; font-weight:800; color:var(--primary); line-height:1;">${percentage}%</div>
          <p style="color:#64748b; font-weight:600; text-transform:uppercase; letter-spacing:1px; font-size:0.85rem; margin-top:5px;">Overall Attendance</p>
          <div style="height:12px; background:#e2e8f0; border-radius:10px; margin-top:20px; overflow:hidden;">
            <div style="height:100%; width:${percentage}%; background:var(--primary); border-radius:10px;"></div>
          </div>
        </div>
        
        <div style="margin-top:20px; border-top:1px solid #e2e8f0; padding-top:20px;">
          <h4 style="margin:0 0 16px 0; color:#0f172a;">Recent Records</h4>
          <div style="max-height:300px; overflow-y:auto; padding-right:10px;">
            ${listHTML}
          </div>
        </div>
      `;
    }
  },
  {
    selector: '.feature-card:nth-child(10)',
    title: 'Apply Leave',
    render: () => {
      window.submitLeave = function(e) {
        e.preventDefault();
        const start = e.target.elements[0].value;
        const end = e.target.elements[1].value;
        const reason = e.target.elements[2].value;
        
        let users = JSON.parse(localStorage.getItem('erp_users')) || {};
        
        if(users[user.mobile]) {
          if(!users[user.mobile].leaveRequests) users[user.mobile].leaveRequests = [];
          users[user.mobile].leaveRequests.push({
            date: start + ' to ' + end,
            reason: reason,
            status: 'Pending'
          });
          localStorage.setItem('erp_users', JSON.stringify(users));
          
          // Update local session
          user = users[user.mobile];
          localStorage.setItem('erp_current_user', JSON.stringify(user));
        }
        
        alert("Leave Request sent to Admin!");
        modalOverlay.classList.remove('active');
      };
      
      // Fetch fresh data from database to show latest approval status
      let allUsers = JSON.parse(localStorage.getItem('erp_users')) || {};
      let freshUser = allUsers[user.mobile] || user;
      
      let pastLeavesHTML = '';
      if(freshUser.leaveRequests && freshUser.leaveRequests.length > 0) {
        freshUser.leaveRequests.slice().reverse().forEach(l => {
          let color = l.status === 'Approved' ? '#10b981' : (l.status === 'Rejected' ? '#ef4444' : '#f59e0b');
          let bg = l.status === 'Approved' ? '#dcfce7' : (l.status === 'Rejected' ? '#fee2e2' : '#fef3c7');
          pastLeavesHTML += `<div style="font-size:0.85rem; padding:12px; background:#f8fafc; border:1px solid #e2e8f0; border-left: 4px solid ${color}; border-radius:8px; margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:4px;">
              <div style="font-weight:700; color:#334155;">${l.date}</div>
              <div style="display:inline-block; padding:3px 10px; border-radius:12px; font-size:0.75rem; font-weight:800; color:${color}; background:${bg};">${l.status}</div>
            </div>
            <div style="color:#64748b; margin-bottom:2px; font-weight:500;">${l.reason}</div>
          </div>`;
        });
      }

      return `
        <form onsubmit="window.submitLeave(event)">
          <div class="leave-form-group">
            <label class="leave-form-label">Start Date</label>
            <input type="date" class="leave-form-input" required>
          </div>
          <div class="leave-form-group">
            <label class="leave-form-label">End Date</label>
            <input type="date" class="leave-form-input" required>
          </div>
          <div class="leave-form-group">
            <label class="leave-form-label">Reason</label>
            <textarea class="leave-form-input" rows="3" required placeholder="Why do you need leave?"></textarea>
          </div>
          <button type="submit" class="btn btn-primary" style="width:100%; padding:12px;">Submit Request</button>
        </form>
        <div style="margin-top:30px; border-top:1px solid #e2e8f0; padding-top:20px;">
          <h4 style="margin:0 0 12px 0;">Leave History</h4>
          ${pastLeavesHTML ? pastLeavesHTML : `<p style="color:#94a3b8; font-size:0.85rem;">You haven't requested any leaves yet.</p>`}
        </div>
      `;
    }
  },
  {
    selector: '.feature-card:nth-child(5)',
    title: 'Daily Timetable',
    render: () => emptyState('fa-solid fa-clock-rotate-left', 'Timetable Pending', 'Your class timetable has not been uploaded by the coordinator yet.')
  },
  {
    selector: '.feature-card:nth-child(6)',
    title: 'Assignments',
    render: () => {
      let allUsers = JSON.parse(localStorage.getItem('erp_users')) || {};
      let freshUser = allUsers[user.mobile] || user;
      let assignments = freshUser.assignments || [];
      
      if(assignments.length === 0) {
        return emptyState('fa-solid fa-clipboard-check', 'Hooray! No Homework', 'You have no pending assignments or worksheets to submit.');
      }
      
      let html = '<div style="display:flex; flex-direction:column; gap:10px;">';
      assignments.forEach(a => {
         html += `<div style="padding:15px; border:1px solid #e2e8f0; border-radius:8px; display:flex; justify-content:space-between; align-items:center; background:#f8fafc;">
            <div>
               <div style="font-weight:700; color:#0f172a;">${a.title}</div>
               <div style="font-size:0.85rem; color:#64748b; margin-top:2px;">${a.subject} • Due: ${a.dueDate}</div>
            </div>
            <div style="font-weight:600; font-size:0.8rem; color:#f59e0b; background:#fef3c7; padding:4px 8px; border-radius:4px;">${a.status}</div>
         </div>`;
      });
      html += '</div>';
      return html;
    }
  },
  {
    selector: '.feature-card:nth-child(7)',
    title: 'My Documents',
    render: () => {
      // Helper to convert file to base64
      window.uploadStudentDoc = function(input, docName) {
        if(input.files && input.files[0]) {
          const file = input.files[0];
          
          // Show loading state on the button
          const label = input.parentElement;
          const originalText = label.innerHTML;
          label.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Uploading...';
          
          const reader = new FileReader();
          reader.onload = function(e) {
            const img = new Image();
            img.onload = function() {
              const canvas = document.createElement('canvas');
              let width = img.width;
              let height = img.height;
              const max_size = 1000;

              if (width > height) {
                if (width > max_size) {
                  height *= max_size / width;
                  width = max_size;
                }
              } else {
                if (height > max_size) {
                  width *= max_size / height;
                  height = max_size;
                }
              }

              canvas.width = width;
              canvas.height = height;
              const ctx = canvas.getContext('2d');
              ctx.drawImage(img, 0, 0, width, height);
              
              // Compress the image aggressively to save localStorage space
              const compressedData = canvas.toDataURL('image/jpeg', 0.6);

              try {
                let allUsers = JSON.parse(localStorage.getItem('erp_users')) || {};
                if(allUsers[user.mobile]) {
                  // Fix array vs object conflict from registration
                  if(!allUsers[user.mobile].documents || Array.isArray(allUsers[user.mobile].documents)) {
                      allUsers[user.mobile].documents = {}; 
                  }
                  
                  allUsers[user.mobile].documents[docName] = compressedData;
                  localStorage.setItem('erp_users', JSON.stringify(allUsers));
                  
                  // Update local session
                  user = allUsers[user.mobile];
                  localStorage.setItem('erp_current_user', JSON.stringify(user));
                  
                  // Refresh Modal
                  document.getElementById('modalBody').innerHTML = modules[7].render();
                }
              } catch(err) {
                 console.error(err);
                 alert("Upload failed! Storage space is full or the image is still too large. Try a smaller file.");
                 label.innerHTML = originalText;
              }
            };
            img.src = e.target.result;
          };
          reader.readAsDataURL(file);
        }
      };

      window.deleteStudentDoc = function(docName) {
        if(confirm("Are you sure you want to delete this document?")) {
           let allUsers = JSON.parse(localStorage.getItem('erp_users')) || {};
           if(allUsers[user.mobile] && allUsers[user.mobile].documents) {
              delete allUsers[user.mobile].documents[docName];
              localStorage.setItem('erp_users', JSON.stringify(allUsers));
              
              user = allUsers[user.mobile];
              localStorage.setItem('erp_current_user', JSON.stringify(user));
              
              document.getElementById('modalBody').innerHTML = modules[7].render();
           }
        }
      };
      
      const docTypes = [
        "Aadhaar Card",
        "Marksheet (10th/Last Class)",
        "Samagra ID",
        "Domicile Certificate (मूल निवासी)",
        "Income Certificate (आय प्रमाण पत्र)",
        "Caste Certificate (जाति प्रमाण पत्र)",
        "Transfer Certificate (TC)",
        "Passport Size Photo"
      ];
      
      let html = `<div style="background:#fef3c7; border:1px solid #fde68a; padding:12px; border-radius:8px; margin-bottom:20px; font-size:0.85rem; color:#d97706; display:flex; gap:10px; align-items:start;">
        <i class="fa-solid fa-triangle-exclamation" style="margin-top:2px;"></i>
        <div>Please upload clear and readable photos of your documents. You can delete and re-upload them if you make a mistake.</div>
      </div>`;
      
      const docs = user.documents || {};
      
      docTypes.forEach(doc => {
        let isUploaded = !!docs[doc];
        let docImage = docs[doc];
        html += `
          <div style="display:flex; justify-content:space-between; align-items:center; padding:16px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; margin-bottom:12px;">
            <div style="font-weight:600; color:#334155; font-size:0.95rem;">
              ${doc}
              ${isUploaded ? `<div style="margin-top:8px;"><img src="${docImage}" style="max-height:60px; border-radius:6px; border:1px solid #cbd5e1;"></div>` : ''}
            </div>
            ${isUploaded ? 
              `<button class="btn-admin-outline" style="color:#ef4444; border-color:#ef4444; padding:6px 12px; font-size:0.85rem;" onclick="window.deleteStudentDoc('${doc}')"><i class="fa-solid fa-trash"></i> Delete</button>` : 
              `<label class="btn btn-outline-primary" style="padding:6px 12px; font-size:0.85rem; cursor:pointer; margin:0;">
                <i class="fa-solid fa-upload"></i> Select Photo
                <input type="file" accept="image/*" style="display:none;" onchange="window.uploadStudentDoc(this, '${doc}')">
              </label>`
            }
          </div>
        `;
      });
      
      return html;
    }
  }
];

// Attach Event Listeners
modules.forEach(mod => {
  const el = document.querySelector(mod.selector);
  if(el && !el.classList.contains('locked-card')) {
    el.addEventListener('click', () => {
      openModal(mod.title, mod.render());
    });
  }
});
