import os

path = r'd:\Gurudev international\Gurudev intenational\js\erp-auth.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CORS headers for Google Apps Script fetch
old_fetch = """      // 2. Google Sheets sync (Dummy URL placeholder)
      const googleSheetsUrl = 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL';
      if(googleSheetsUrl !== 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL') {
        fetch(googleSheetsUrl, {
          method: 'POST',
          mode: 'no-cors',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData)
        }).catch(err => console.log('GSheets sync failed:', err));
      }"""

new_fetch = """      // 2. Google Sheets sync (Dummy URL placeholder)
      const googleSheetsUrl = 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL';
      if(googleSheetsUrl !== 'YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL') {
        fetch(googleSheetsUrl, {
          method: 'POST',
          // Send as text/plain to avoid CORS Preflight request block from Google Apps Script
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(userData)
        }).then(response => console.log('GSheets sync requested'))
          .catch(err => console.log('GSheets sync failed:', err));
      }"""

if "mode: 'no-cors'," in content:
    content = content.replace(old_fetch, new_fetch)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated Google Sheets fetch logic in erp-auth.js")
