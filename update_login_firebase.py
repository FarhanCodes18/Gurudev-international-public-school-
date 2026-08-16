import os

path = r'd:\Gurudev international\Gurudev intenational\js\erp-auth.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add getDoc to imports
old_imports = """import { db, storage } from './firebase-config.js';
import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';"""
new_imports = """import { db, storage } from './firebase-config.js';
import { doc, setDoc, getDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';"""

if 'getDoc' not in content:
    content = content.replace(old_imports, new_imports)

# Replace login logic
old_login = """      // Admin bypass
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
      localStorage.setItem('erp_current_user', JSON.stringify(user));"""

new_login = """      // Seed Admin credentials to Firebase if not exists (To ensure it never gets deleted)
      if (mobile === 'admin' || mobile.includes('@admin')) {
         if(db) {
            const adminDoc = await getDoc(doc(db, "admins", "admin"));
            if(!adminDoc.exists()) {
               await setDoc(doc(db, "admins", "admin"), {
                  role: "admin",
                  mobile: "admin",
                  password: "admin", // Default password, user should change this in DB
                  name: "Super Admin"
               });
            }
            
            // Verify Admin Login
            const adminCheck = await getDoc(doc(db, "admins", "admin"));
            if(adminCheck.exists() && adminCheck.data().password === password) {
               localStorage.setItem('erp_current_user', JSON.stringify(adminCheck.data()));
               showAlert("Admin login successful! Redirecting...", "success");
               setTimeout(() => { window.location.href = "erp-admin.html"; }, 1000);
               return;
            } else {
               throw new Error("Incorrect Admin Password.");
            }
         } else {
            // Fallback if Firebase not setup
            if(password === 'admin') {
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

      if (user.password !== password) {
        throw new Error("Incorrect password.");
      }

      // Create Session
      localStorage.setItem('erp_current_user', JSON.stringify(user));"""

content = content.replace(old_login, new_login)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated login logic with Firebase read and Admin seeding.")
