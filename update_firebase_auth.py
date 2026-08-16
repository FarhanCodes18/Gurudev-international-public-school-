import os

path = r'd:\Gurudev international\Gurudev intenational\js\erp-auth.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_imports = """import { db, storage } from './firebase-config.js';
import { doc, setDoc, getDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';
import { ref, uploadString, getDownloadURL } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js';"""

new_imports = """import { auth, db, storage } from './firebase-config.js';
import { doc, setDoc, getDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';
import { ref, uploadString, getDownloadURL } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js';
import { createUserWithEmailAndPassword, signInWithEmailAndPassword, sendPasswordResetEmail } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js';"""

if 'createUserWithEmailAndPassword' not in content:
    content = content.replace(old_imports, new_imports)

# 2. Update Registration
old_register_logic = """      // Auto-login after registration
      localStorage.setItem('erp_current_user', JSON.stringify(userData));
      showAlert("Registration successful! Redirecting to Dashboard...", "success");"""

new_register_logic = """      // Auto-login after registration
      if(auth) {
         try {
            await createUserWithEmailAndPassword(auth, email, password);
         } catch(authErr) {
            console.error("Firebase Auth Error:", authErr);
            throw new Error("Registration failed: " + authErr.message);
         }
      }
      localStorage.setItem('erp_current_user', JSON.stringify(userData));
      showAlert("Registration successful! Redirecting to Dashboard...", "success");"""

if 'createUserWithEmailAndPassword' not in content:
    content = content.replace(old_register_logic, new_register_logic)

# 3. Update Login
old_login_logic = """            // Verify Admin Login
            const adminCheck = await getDoc(doc(db, "admins", "admin"));
            if(adminCheck.exists() && adminCheck.data().password === password) {
               localStorage.setItem('erp_current_user', JSON.stringify(adminCheck.data()));
               showAlert("Admin login successful! Redirecting...", "success");
               setTimeout(() => { window.location.href = "erp-admin.html"; }, 1000);
               return;
            } else {
               throw new Error("Incorrect Admin Password.");
            }"""

new_login_logic = """            // Verify Admin Login using Auth
            try {
               await signInWithEmailAndPassword(auth, "admin@gurudev.com", password);
               localStorage.setItem('erp_current_user', JSON.stringify(adminCheck.data()));
               showAlert("Admin login successful! Redirecting...", "success");
               setTimeout(() => { window.location.href = "erp-admin.html"; }, 1000);
               return;
            } catch (err) {
               throw new Error("Incorrect Admin Password.");
            }"""

if 'signInWithEmailAndPassword(auth, "admin@gurudev.com"' not in content:
    content = content.replace(old_login_logic, new_login_logic)

old_student_login = """      if (!user) {
        throw new Error("Account not found. Please register first.");
      }

      if (user.password !== password) {
        throw new Error("Incorrect password.");
      }"""

new_student_login = """      if (!user) {
        throw new Error("Account not found. Please register first.");
      }

      if(auth && user.email) {
         try {
            await signInWithEmailAndPassword(auth, user.email, password);
         } catch(err) {
            throw new Error("Incorrect email or password.");
         }
      } else {
         if (user.password !== password) {
            throw new Error("Incorrect password.");
         }
      }"""

if 'signInWithEmailAndPassword(auth, user.email' not in content:
    content = content.replace(old_student_login, new_student_login)


# 4. Forgot Password Logic
forgot_password_logic = """

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
"""

if 'forgotPasswordLink' not in content:
    content += forgot_password_logic


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated erp-auth.js with real Firebase Authentication!")
