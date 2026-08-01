// --- LOCAL STORAGE DATABASE ENGINE ---
// This replaces Firebase to provide a working A-Z experience locally.

function showAlert(message, type) {
  const alertEl = document.getElementById('authAlert');
  if (!alertEl) return;
  alertEl.style.display = 'block';
  alertEl.className = 'erp-alert erp-alert-' + type;
  alertEl.textContent = message;
}

function generateStudentId(classNum) {
  const year = new Date().getFullYear();
  const randomStr = Math.floor(100 + Math.random() * 900);
  return `IPS-${year % 100}-${classNum}-${randomStr}`;
}

// Convert image file to Base64 to store in localStorage
function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
}

// --- Registration Logic ---
const registerForm = document.getElementById('registerForm');
if (registerForm) {
  registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('btnRegister');
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Registering...';
    btn.disabled = true;

    try {
      const name = document.getElementById('regName').value;
      const mobile = document.getElementById('regMobile').value;
      const email = document.getElementById('regEmail').value;
      const studentClass = document.getElementById('regClass').value;
      const gender = document.getElementById('regGender').value;
      const dob = document.getElementById('regDob').value;
      const password = document.getElementById('regPassword').value;
      const photoInput = document.getElementById('regPhoto');

      // Check if user already exists
      let users = JSON.parse(localStorage.getItem('erp_users')) || {};
      if (users[mobile]) {
        throw new Error("Mobile number already registered. Please login.");
      }

      let photoURL = "assets/images/default-avatar.png";
      if (photoInput.files.length > 0) {
        photoURL = await getBase64(photoInput.files[0]);
      }

      const studentId = generateStudentId(studentClass);
      
      const userData = {
        role: "student",
        studentId: studentId,
        name: name,
        mobile: mobile,
        email: email,
        class: studentClass,
        gender: gender,
        dob: dob,
        photoURL: photoURL,
        password: password, // Storing plaintext for local simulation
        registrationDate: new Date().toISOString(),
        attendance: 0,
        badges: [],
        leaves: [],
        assignments: [],
        documents: []
      };

      // Save to "DB"
      users[mobile] = userData;
      localStorage.setItem('erp_users', JSON.stringify(users));

      showAlert("Registration successful! Redirecting to login...", "success");
      setTimeout(() => {
        window.location.href = "erp-login.html";
      }, 1500);

    } catch (error) {
      showAlert(error.message, "error");
      btn.innerHTML = 'Register Student';
      btn.disabled = false;
    }
  });

  const photoInput = document.getElementById('regPhoto');
  if(photoInput) {
    photoInput.addEventListener('change', (e) => {
      if(e.target.files.length > 0) {
        document.getElementById('uploadText').innerHTML = `<i class="fa-solid fa-check" style="color:#16a34a"></i> Image Selected`;
      }
    });
  }
}

// --- Login Logic ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('btnLogin');
    btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Logging in...';
    btn.disabled = true;

    try {
      const mobile = document.getElementById('loginEmail').value.trim();
      const password = document.getElementById('loginPassword').value;

      // Admin bypass
      if(mobile === 'admin' || mobile.includes('@admin')) {
         window.location.href = "erp-admin.html";
         return;
      }

      let users = JSON.parse(localStorage.getItem('erp_users')) || {};
      const user = users[mobile];

      if (!user) {
        throw new Error("Account not found. Please register first.");
      }

      if (user.password !== password) {
        throw new Error("Incorrect password.");
      }

      // Create Session
      localStorage.setItem('erp_current_user', JSON.stringify(user));
      showAlert("Login successful! Redirecting...", "success");
      
      setTimeout(() => {
        window.location.href = "erp-dashboard.html";
      }, 1000);

    } catch (error) {
      showAlert(error.message, "error");
      btn.innerHTML = '<i class="fa-solid fa-lock"></i> Login to Portal';
      btn.disabled = false;
    }
  });
}
