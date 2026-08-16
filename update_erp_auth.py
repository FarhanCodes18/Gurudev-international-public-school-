import os
import re

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'js', 'erp-auth.js')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Import Firebase at the top
firebase_imports = """import { db } from './firebase-config.js';
import { doc, setDoc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';\n
"""

if "import { db }" not in content:
    content = firebase_imports + content

# Replace the Firebase Database sync (Dummy URL placeholder) logic with actual Firestore SDK logic
old_fb_logic = """      // 3. Firebase Database sync (Dummy URL placeholder)
      const firebaseDbUrl = 'YOUR_FIREBASE_DATABASE_URL/students.json';
      if(firebaseDbUrl !== 'YOUR_FIREBASE_DATABASE_URL/students.json') {
        fetch(firebaseDbUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData)
        }).catch(err => console.log('Firebase sync failed:', err));
      }"""

new_fb_logic = """      // 3. Save to Firebase Firestore Database
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
      }"""

content = content.replace(old_fb_logic, new_fb_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated erp-auth.js to save to Firestore")
