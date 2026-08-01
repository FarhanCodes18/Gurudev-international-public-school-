import { app, auth, db } from './firebase-config.js';
import { onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { collection, query, where, onSnapshot } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

// --- SPA Navigation Logic ---
const navItems = document.querySelectorAll('.erp-nav-item[data-target]');
const modules = document.querySelectorAll('.erp-module');
const pageTitle = document.getElementById('pageTitle');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const sidebar = document.getElementById('erpSidebar');

navItems.forEach(item => {
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    modules.forEach(mod => mod.classList.remove('active'));
    item.classList.add('active');
    const targetId = item.getAttribute('data-target');
    document.getElementById(targetId).classList.add('active');
    pageTitle.textContent = item.textContent.trim();
    if(window.innerWidth <= 768) { sidebar.classList.remove('show'); }
  });
});

if(mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', () => { sidebar.classList.toggle('show'); });
}

// --- Firebase Realtime Data & Auth ---
const tableBody = document.getElementById('studentsTableBody');
const countTotal = document.getElementById('totalStudentsCount');
const countPending = document.getElementById('pendingApprovalsCount');

function renderMockData() {
  console.log("Mock Mode Active: Rendering dummy students table.");
  countTotal.textContent = "3";
  countPending.textContent = "1";
  
  const mockStudents = [
    { id: "GI20261001", name: "Rahul Sharma", class: "10", mobile: "9876543210", plainPassword: "rahulpassword", status: "Active", photoURL: "assets/images/default-avatar.png" },
    { id: "GI20261002", name: "Priya Singh", class: "12", mobile: "8765432109", plainPassword: "priya!123", status: "Active", photoURL: "assets/images/default-avatar.png" },
    { id: "GI20261003", name: "Amit Kumar", class: "9", mobile: "7654321098", plainPassword: "amitsecure", status: "Pending", photoURL: "assets/images/default-avatar.png" }
  ];

  tableBody.innerHTML = "";
  mockStudents.forEach(doc => {
    tableBody.innerHTML += `
      <tr>
        <td><img src="${doc.photoURL}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;"></td>
        <td style="font-weight:600; color:var(--primary);">${doc.id}</td>
        <td>${doc.name}</td>
        <td>${doc.class}</td>
        <td>${doc.mobile}</td>
        <td class="reveal-password">${doc.plainPassword}</td>
        <td><span class="status-badge ${doc.status === 'Active' ? 'status-active' : 'status-pending'}">${doc.status}</span></td>
        <td>
          <button class="action-btn" title="Edit"><i class="fa-solid fa-pen-to-square"></i></button>
          <button class="action-btn" title="Approve"><i class="fa-solid fa-check"></i></button>
          <button class="action-btn" title="Delete" style="color:#ef4444;"><i class="fa-solid fa-trash"></i></button>
        </td>
      </tr>
    `;
  });
}

if (app) {
  onAuthStateChanged(auth, (user) => {
    if (user) {
      // Listen to users collection for students
      const q = query(collection(db, "users"), where("role", "==", "student"));
      
      try {
        onSnapshot(q, (querySnapshot) => {
          let total = 0;
          let pending = 0;
          tableBody.innerHTML = "";

          if(querySnapshot.empty) {
            tableBody.innerHTML = `<tr><td colspan="8" style="text-align:center;">No students found.</td></tr>`;
            countTotal.textContent = "0";
            countPending.textContent = "0";
            return;
          }

          querySnapshot.forEach((docSnap) => {
            const data = docSnap.data();
            total++;
            if (data.status === "Pending") pending++;

            const statusClass = data.status === "Active" ? "status-active" : "status-pending";
            const photo = data.photoURL || "assets/images/default-avatar.png";

            tableBody.innerHTML += `
              <tr>
                <td><img src="${photo}" style="width:36px; height:36px; border-radius:50%; object-fit:cover;"></td>
                <td style="font-weight:600; color:var(--primary);">${data.studentId || 'N/A'}</td>
                <td>${data.name}</td>
                <td>${data.class}</td>
                <td>${data.mobile}</td>
                <td class="reveal-password">${data.plainPassword || 'Hidden'}</td>
                <td><span class="status-badge ${statusClass}">${data.status}</span></td>
                <td>
                  <button class="action-btn" title="Edit"><i class="fa-solid fa-pen-to-square"></i></button>
                  <button class="action-btn" title="Approve"><i class="fa-solid fa-check"></i></button>
                </td>
              </tr>
            `;
          });

          countTotal.textContent = total;
          countPending.textContent = pending;
        }, (error) => {
          console.error("Firestore onSnapshot error. Reverting to mock data.", error);
          renderMockData(); // Fallback if Firebase rules block or fail
        });
      } catch(e) {
         renderMockData();
      }

    } else {
      window.location.href = "erp-login.html";
    }
  });
} else {
  renderMockData();
}

// --- Logout ---
const btnLogout = document.getElementById('btnLogout');
if (btnLogout) {
  btnLogout.addEventListener('click', () => {
    if (app) {
      signOut(auth).then(() => window.location.href = "erp-login.html");
    } else {
      window.location.href = "erp-login.html";
    }
  });
}
