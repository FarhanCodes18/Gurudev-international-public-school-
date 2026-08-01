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
    render: () => emptyState('fa-regular fa-calendar-xmark', 'No Upcoming Events', 'There are no holidays or events scheduled for this month.')
  },
  {
    selector: '.feature-card:nth-child(3)',
    title: 'My Attendance',
    render: () => `
      <div style="text-align:center; padding: 20px;">
        <div style="font-size: 3rem; font-weight:800; color:#94a3b8;">${user.attendance || 0}%</div>
        <p style="color:#64748b; font-weight:500;">Overall Attendance</p>
        <div style="height:12px; background:#e2e8f0; border-radius:10px; margin-top:20px; overflow:hidden;">
          <div style="height:100%; width:${user.attendance || 0}%; background:var(--primary); border-radius:10px;"></div>
        </div>
        <p style="color:#94a3b8; font-size:0.85rem; margin-top:16px;"><i class="fa-solid fa-circle-info"></i> Attendance tracking hasn't started for your profile yet.</p>
      </div>
    `
  },
  {
    selector: '.feature-card:nth-child(4)',
    title: 'Apply Leave',
    render: () => {
      window.submitLeave = function(e) {
        e.preventDefault();
        const start = e.target.elements[0].value;
        const end = e.target.elements[1].value;
        const reason = e.target.elements[2].value;
        
        let users = JSON.parse(localStorage.getItem('erp_users'));
        let uIdx = users.findIndex(u => u.phone === user.mobile);
        
        if(uIdx > -1) {
          if(!users[uIdx].leaveRequests) users[uIdx].leaveRequests = [];
          users[uIdx].leaveRequests.push({
            date: start + ' to ' + end,
            reason: reason,
            status: 'Pending'
          });
          localStorage.setItem('erp_users', JSON.stringify(users));
          
          // Update local session
          user = users[uIdx];
          localStorage.setItem('erp_current_user', JSON.stringify(user));
        }
        
        alert("Leave Request sent to Admin!");
        modalOverlay.classList.remove('active');
      };
      
      let pastLeavesHTML = '';
      if(user.leaveRequests && user.leaveRequests.length > 0) {
        user.leaveRequests.slice().reverse().forEach(l => {
          let color = l.status === 'Approved' ? '#10b981' : (l.status === 'Rejected' ? '#ef4444' : '#f59e0b');
          pastLeavesHTML += `<div style="font-size:0.85rem; padding:12px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; margin-bottom:8px;">
            <div style="font-weight:600; margin-bottom:4px;">${l.date}</div>
            <div style="color:#64748b; margin-bottom:6px;">${l.reason}</div>
            <div style="display:inline-block; padding:2px 8px; border-radius:12px; font-size:0.7rem; font-weight:700; color:${color}; background:${color}20;">${l.status}</div>
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
    title: 'Transport Routes',
    render: () => emptyState('fa-solid fa-bus-simple', 'No Route Assigned', 'You are not assigned to any school transport route. Please contact the transport admin.')
  },
  {
    selector: '.feature-card:nth-child(6)',
    title: 'Daily Timetable',
    render: () => emptyState('fa-solid fa-clock-rotate-left', 'Timetable Pending', 'Your class timetable has not been uploaded by the coordinator yet.')
  },
  {
    selector: '.feature-card:nth-child(7)',
    title: 'Assignments',
    render: () => emptyState('fa-solid fa-clipboard-check', 'Hooray! No Homework', 'You have no pending assignments or worksheets to submit.')
  },
  {
    selector: '.feature-card:nth-child(8)',
    title: 'My Documents',
    render: () => {
      window.uploadDoc = function(input) {
        if(input.files.length > 0) {
          alert(`Simulated Upload: ${input.files[0].name} saved successfully!`);
        }
      };
      
      return `
        ${emptyState('fa-regular fa-folder-open', 'No Documents', 'Upload your Aadhaar card, past marksheets, or medical certificates.')}
        <div style="margin-top:24px;">
          <label style="display:block; padding:20px; border:2px dashed #cbd5e1; border-radius:12px; text-align:center; cursor:pointer; background:#f8fafc; transition:0.2s;">
            <i class="fa-solid fa-cloud-arrow-up" style="font-size:1.5rem; color:var(--primary); margin-bottom:8px;"></i><br>
            <strong>Click to Upload Document</strong>
            <input type="file" style="display:none;" onchange="window.uploadDoc(this)">
          </label>
        </div>
      `;
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
