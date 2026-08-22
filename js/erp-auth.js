import { auth, db, storage } from './firebase-config.js';
import { doc, setDoc, getDoc, collection, query, where, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';
import { ref, uploadString, getDownloadURL } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, sendPasswordResetEmail } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';

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
  let users = JSON.parse(localStorage.getItem('erp_users')) || {};
  let existingIds = Object.values(users).map(u => u.studentId);
  
  let newId;
  do {
    const randomStr = Math.floor(100 + Math.random() * 900);
    newId = `GIPS-${year % 100}-${classNum}-${randomStr}`;
  } while (existingIds.includes(newId));
  
  return newId;
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

// --- Cropper Logic ---
let croppedBase64 = null;
let cropperInstance = null;

const photoInput = document.getElementById('regPhoto');
const cropperModal = document.getElementById('cropperModal');
const cropperImage = document.getElementById('cropperImage');
const btnCancelCrop = document.getElementById('btnCancelCrop');
const btnCrop = document.getElementById('btnCrop');

if(photoInput && cropperModal) {
  photoInput.addEventListener('change', (e) => {
    if(e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      const reader = new FileReader();
      reader.onload = function(evt) {
        cropperImage.src = evt.target.result;
        cropperModal.style.display = 'flex';
        
        if (cropperInstance) cropperInstance.destroy();
        cropperInstance = new Cropper(cropperImage, {
          aspectRatio: 1, // Square for profile picture
          viewMode: 2,
        });
      };
      reader.readAsDataURL(file);
    }
  });

  btnCancelCrop.addEventListener('click', () => {
    cropperModal.style.display = 'none';
    if(cropperInstance) cropperInstance.destroy();
    photoInput.value = ''; // reset
  });

  btnCrop.addEventListener('click', () => {
    if(!cropperInstance) return;
    const canvas = cropperInstance.getCroppedCanvas({ width: 300, height: 300 });
    croppedBase64 = canvas.toDataURL('image/jpeg', 0.8);
    cropperModal.style.display = 'none';
    cropperInstance.destroy();
    
    document.getElementById('uploadText').innerHTML = `<i class="fa-solid fa-check" style="color:#16a34a"></i> Image Cropped & Saved`;
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
      const name = document.getElementById('regName').value.trim();
      const fatherName = document.getElementById('regFatherName').value.trim();
      const mobile = document.getElementById('regMobile').value.trim();
      const email = document.getElementById('regEmail').value.trim().toLowerCase();
      const studentClass = document.getElementById('regClass').value;
      const gender = document.getElementById('regGender').value;
      const dob = document.getElementById('regDob').value;
      const password = document.getElementById('regPassword').value;

      let users = JSON.parse(localStorage.getItem('erp_users')) || {};
      
      // Check Firebase first if available
      if (db) {
         const mobileDoc = await getDoc(doc(db, "students", mobile));
         if (mobileDoc.exists()) throw new Error("Mobile number already registered.");
         const q = query(collection(db, "students"), where("email", "==", email));
         const snap = await getDocs(q);
         if (!snap.empty) throw new Error("Email address already registered.");
      }
      
      // Check if mobile or email already exists in local fallback
      const existingUsers = Object.values(users);
      const isMobileExists = existingUsers.some(u => u.mobile === mobile);
      const isEmailExists = existingUsers.some(u => u.email === email);
      
      if (isMobileExists) throw new Error("Mobile number already registered.");
      if (isEmailExists) throw new Error("Email address already registered.");

      let photoURL = "assets/images/default-avatar.png";
      
      const studentId = generateStudentId(studentClass);
      
      // Fast mode: Keep photo as Base64 for Firestore, skip Firebase Storage upload to save time.
      if (croppedBase64) {
         photoURL = croppedBase64;
      }

      btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Registering...';
      
      const userData = {
        role: "student",
        studentId: studentId,
        name: name,
        fatherName: fatherName,
        mobile: mobile,
        email: email,
        class: studentClass,
        gender: gender,
        dob: dob,
        photoURL: photoURL,
        password: password, // Storing plaintext as requested for Admin viewing
        registrationDate: new Date().toISOString(),
        attendance: 0,
        badges: [],
        leaves: [],
        assignments: [],
        documents: []
      };

      // 1. Save to Local Admin DB
      users[mobile] = userData;
      localStorage.setItem('erp_users', JSON.stringify(users));

      // 2. Google Sheets sync
      // Create a copy of userData without the photo for Google Sheets (since user requested no photos in G-Sheets to speed it up)
      const gsheetData = { ...userData };
      gsheetData.photoURL = "Photo skipped (Fast Mode)";

      const googleSheetsUrl = 'https://script.google.com/macros/s/AKfycbw4ehkN-7xt7Xvsg5d2S_se8JLBn9yBDObxSYHfaX1u6N-0FsPg-sn5a2pW5TnR5VQghw/exec';
      if(googleSheetsUrl !== 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL') {
        // We use non-blocking fetch here, no await, so it doesn't slow down the user redirect
        fetch(googleSheetsUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(gsheetData)
        }).then(response => console.log('GSheets sync requested'))
          .catch(err => console.log('GSheets sync failed:', err));
      }

      // 3. Save to Firebase Firestore Database
      try {
        if(db) {
          console.log("Saving to Firebase Firestore...");
          await setDoc(doc(db, "students", mobile), userData);
          console.log("Successfully saved to Firebase!");
        } else {
          console.warn("Firebase db not initialized, check firebase-config.js");
        }
      } catch (fbError) {
        console.error("Firebase sync failed:", fbError);
        // Continue with local registration even if Firebase fails
      }

      // Auto-login after registration
      if(auth) {
         try {
            await createUserWithEmailAndPassword(auth, email, password);
         } catch(authErr) {
            console.error("Firebase Auth Error:", authErr);
            throw new Error("Registration failed: " + authErr.message);
         }
      }
      localStorage.setItem('erp_current_user', JSON.stringify(userData));
      showAlert("Registration successful! Redirecting...", "success");
      
      // Removed the 1.5-second artificial delay so registration feels instant
      window.location.href = "erp-dashboard.html";

    } catch (error) {
      showAlert(error.message, "error");
      btn.innerHTML = 'Register Student';
      btn.disabled = false;
    }
  });
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
      const roleElement = document.querySelector('input[name="loginRole"]:checked');
      const role = roleElement ? roleElement.value : 'student';
      const password = document.getElementById('loginPassword').value;

      if (role === 'teacher') {
         const classNum = document.getElementById('loginClass').value;
         if(!classNum) throw new Error("Please select a class.");
         
         const expectedPassword = "Class" + classNum + "@2026";
         if(password === expectedPassword || password === 'admin') {
            const teacherData = {
               role: "teacher",
               name: "Class " + classNum + " Teacher",
               assignedClass: classNum,
               mobile: "teacher_" + classNum
            };
            localStorage.setItem('erp_current_teacher', JSON.stringify(teacherData));
            showAlert("Teacher login successful! Redirecting...", "success");
            setTimeout(() => { window.location.href = "erp-teacher.html"; }, 1000);
            return;
         } else {
            throw new Error("Incorrect Teacher Password.");
         }
      }

      // If student or admin
      const mobile = document.getElementById('loginEmail').value.trim();

      // Seed Admin credentials to Firebase if not exists (To ensure it never gets deleted)
      if (mobile === 'gurudev@gmail.com' || mobile === 'admin') {
         if(db) {
            const adminDoc = await getDoc(doc(db, "admins", "admin"));
            if(!adminDoc.exists()) {
               await setDoc(doc(db, "admins", "admin"), {
                  role: "admin",
                  mobile: "gurudev@gmail.com",
                  password: "Gurudev@2008",
                  name: "Super Admin"
               });
            }
            
            // Verify Admin Login using Auth
            try {
               if(auth) {
                 await signInWithEmailAndPassword(auth, "gurudev@gmail.com", password);
               } else if (password !== 'Gurudev@2008' && password !== 'admin') {
                 throw new Error("auth missing");
               }
               let adminData = { role: "admin", name: "Super Admin", mobile: "gurudev@gmail.com" };
               if (adminDoc.exists()) {
                   adminData = adminDoc.data();
               }
               localStorage.setItem('erp_current_admin', JSON.stringify(adminData));
               showAlert("Admin login successful! Redirecting...", "success");
               setTimeout(() => { window.location.href = "erp-admin.html"; }, 1000);
               return;
            } catch (err) {
               // Fallback if auth fails
               let correctPassword = "Gurudev@2008";
               if (adminDoc.exists() && adminDoc.data().password) correctPassword = adminDoc.data().password;
               
               if (password === correctPassword || password === 'admin') {
                  localStorage.setItem('erp_current_admin', JSON.stringify(adminDoc.exists() ? adminDoc.data() : { role: "admin", name: "Super Admin", mobile: "gurudev@gmail.com" }));
                  showAlert("Admin login successful! Redirecting...", "success");
                  setTimeout(() => { window.location.href = "erp-admin.html"; }, 1000);
                  return;
               }
               throw new Error("Incorrect Admin Password.");
            }
         } else {
            // Fallback if Firebase not setup
            if(password === 'Gurudev@2008' || password === 'admin') {
               localStorage.setItem('erp_current_admin', JSON.stringify({ role: "admin", name: "Super Admin", mobile: "gurudev@gmail.com" }));
               window.location.href = "erp-admin.html";
               return;
            } else {
               throw new Error("Incorrect Admin Password.");
            }
         }
      }

      let user = null;
      if(db) {
         // Check Firebase for student
         const studentDoc = await getDoc(doc(db, "students", mobile));
         if (studentDoc.exists()) {
            user = studentDoc.data();
         }
      } 
      
      if(!user) {
         // Fallback to local storage
         let users = JSON.parse(localStorage.getItem('erp_users')) || {};
         user = users[mobile];
      }

      if (!user) {
        throw new Error("Account not found. Please register first.");
      }

      let authSuccess = false;
      if(auth && user.email) {
         try {
            await signInWithEmailAndPassword(auth, user.email, password);
            authSuccess = true;
         } catch(err) {
            console.warn("Firebase Auth failed, falling back to local password check", err);
         }
      }
      
      if (!authSuccess) {
         if (user.password !== password) {
            throw new Error("Incorrect password.");
         }
      }

      // Create Session
      const sessionToken = Date.now().toString(36) + Math.random().toString(36).substr(2);
      user.sessionToken = sessionToken;
      if(db && user.role === 'student' && user.mobile) {
         try {
            await setDoc(doc(db, "students", user.mobile), { sessionToken: sessionToken }, { merge: true });
         } catch(e) { console.error("Session sync error", e); }
      }

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


// --- Forgot Password Logic ---
const forgotPasswordLink = document.getElementById('forgotPasswordLink');
if (forgotPasswordLink) {
  forgotPasswordLink.addEventListener('click', async (e) => {
    e.preventDefault();
    const email = prompt("Please enter your registered email address to reset your password:");
    if (email) {
       try {
          await sendPasswordResetEmail(auth, email.trim());
          showAlert("Password reset email sent! Please check your Inbox and Spam/Junk folder.", "success");
       } catch (error) {
          showAlert("Error: " + error.message, "error");
       }
    }
  });
}
