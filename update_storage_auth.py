import re

path = r'd:\Gurudev international\Gurudev intenational\js\erp-auth.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update imports
old_imports = """import { db } from './firebase-config.js';
import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';"""

new_imports = """import { db, storage } from './firebase-config.js';
import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';
import { ref, uploadString, getDownloadURL } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js';"""

content = content.replace(old_imports, new_imports)

# 2. Update logic inside registerForm submit
old_photo_logic = """      let photoURL = "assets/images/default-avatar.png";
      if (croppedBase64) {
        photoURL = croppedBase64;
      }

      const studentId = generateStudentId(studentClass);
      
      const userData = {"""

new_photo_logic = """      let photoURL = "assets/images/default-avatar.png";
      
      const studentId = generateStudentId(studentClass);
      
      // Upload to Firebase Storage if we have a cropped image
      if (croppedBase64 && storage) {
        try {
          btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Uploading Photo...';
          const storageRef = ref(storage, `student_photos/${studentId}_${Date.now()}.jpg`);
          // Extract base64 data correctly (remove data:image/jpeg;base64, part)
          const uploadResult = await uploadString(storageRef, croppedBase64, 'data_url');
          photoURL = await getDownloadURL(uploadResult.ref);
          console.log("Photo uploaded to Firebase Storage:", photoURL);
        } catch(err) {
          console.error("Firebase Storage Upload Failed:", err);
          console.log("Continuing with default photo or base64 due to storage error.");
          // Fallback just in case rules block it
          photoURL = croppedBase64; 
        }
      } else if (croppedBase64) {
         photoURL = croppedBase64;
      }

      btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Registering...';
      
      const userData = {"""

content = content.replace(old_photo_logic, new_photo_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated erp-auth.js for Firebase Storage upload")
