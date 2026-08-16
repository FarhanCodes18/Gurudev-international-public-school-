import os

path = r'd:\Gurudev international\Gurudev intenational\js\erp-auth.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_logic = """      // Auto-login after registration
      localStorage.setItem('erp_current_user', JSON.stringify(userData));
      showAlert("Registration successful! Redirecting to Dashboard...", "success");
      
      setTimeout(() => {
        window.location.href = "erp-dashboard.html";
      }, 1500);"""

new_logic = """      // Auto-login after registration
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
      window.location.href = "erp-dashboard.html";"""

if 'createUserWithEmailAndPassword(auth, email, password)' not in content:
    content = content.replace(old_logic, new_logic)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed registration speed and added Firebase Auth creation.")
else:
    print("Auth already present, just fixing timeout.")
    old_timeout = """setTimeout(() => {
        window.location.href = "erp-dashboard.html";
      }, 1500);"""
    new_timeout = """window.location.href = "erp-dashboard.html";"""
    content = content.replace(old_timeout, new_timeout)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
