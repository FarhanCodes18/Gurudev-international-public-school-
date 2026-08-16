import os

path = r'd:\Gurudev international\Gurudev intenational\js\erp-auth.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_photo_logic = """      // Upload to Firebase Storage if we have a cropped image
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
      }"""

new_photo_logic = """      // Fast mode: Keep photo as Base64 for Firestore, skip Firebase Storage upload to save time.
      if (croppedBase64) {
         photoURL = croppedBase64;
      }"""

if '// Upload to Firebase Storage' in content:
    content = content.replace(old_photo_logic, new_photo_logic)


# Now we must ensure Google Sheets doesn't get the massive Base64 string, as requested by user.
old_fetch_logic = """      // 2. Google Sheets sync (Dummy URL placeholder)
      const googleSheetsUrl = 'https://script.google.com/macros/s/AKfycbw4ehkN-7xt7Xvsg5d2S_se8JLBn9yBDObxSYHfaX1u6N-0FsPg-sn5a2pW5TnR5VQghw/exec';
      if(googleSheetsUrl !== 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL') {
        fetch(googleSheetsUrl, {
          method: 'POST',
          // Send as text/plain to avoid CORS Preflight request block from Google Apps Script
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(userData)
        }).then(response => console.log('GSheets sync requested'))
          .catch(err => console.log('GSheets sync failed:', err));
      }"""

new_fetch_logic = """      // 2. Google Sheets sync
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
      }"""

if 'const gsheetData =' not in content:
    content = content.replace(old_fetch_logic, new_fetch_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed slow Firebase Storage upload and excluded photo from Google Sheets.")
