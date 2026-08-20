import os
import re

base_path = r"d:\Gurudev international\Gurudev intenational"

# 1. Update erp-dashboard.html
dashboard_path = os.path.join(base_path, "erp-dashboard.html")
with open(dashboard_path, "r", encoding="utf-8") as f:
    dash_html = f.read()

# I will extract the grid content and replace it manually to be safe.
new_grid = """    <div class="erp-features-grid">
      <!-- 1: Achievement Badges -->
      <div class="feature-card border-yellow" style="animation-delay: 0.1s;">
        <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-trophy"></i></div>
        <div class="text-box">
          <h3>Achievement Badges</h3>
          <p class="text-green">View Certificates</p>
        </div>
      </div>
      <!-- 2: School Calendar -->
      <div class="feature-card border-purple" style="animation-delay: 0.15s;">
        <div class="icon-box bg-purple-light text-purple"><i class="fa-regular fa-calendar"></i></div>
        <div class="text-box">
          <h3>School Calendar</h3>
          <p>Holidays & Events</p>
        </div>
      </div>
      <!-- 3: My Attendance -->
      <div class="feature-card border-blue" style="animation-delay: 0.2s;">
        <div class="icon-box bg-blue-light text-blue"><i class="fa-regular fa-calendar-check"></i></div>
        <div class="text-box">
          <h3>My Attendance</h3>
          <p>Check daily status</p>
        </div>
      </div>
      <!-- 4: Transport Routes (was 5) -->
      <div class="feature-card border-yellow" onclick="openTransportModal()" style="cursor:pointer; animation-delay: 0.25s;">
        <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>
        <div class="text-box">
          <h3>Transport Routes</h3>
          <p>Bus & Driver info</p>
        </div>
      </div>
      <!-- 5: Timetable (was 6) -->
      <div class="feature-card border-red" style="animation-delay: 0.3s;">
        <div class="icon-box bg-red-light text-red"><i class="fa-regular fa-clock"></i></div>
        <div class="text-box">
          <h3>Timetable</h3>
          <p>Daily schedule</p>
        </div>
      </div>
      <!-- 6: Assignments (was 7) -->
      <div class="feature-card border-teal" style="animation-delay: 0.35s;">
        <div class="icon-box bg-teal-light text-teal"><i class="fa-solid fa-book-open"></i></div>
        <div class="text-box">
          <h3>Assignments</h3>
          <p>Pending homework</p>
        </div>
      </div>
      <!-- 7: My Documents (was 8) -->
      <div class="feature-card border-orange" style="animation-delay: 0.4s;">
        <div class="icon-box bg-orange-light text-orange"><i class="fa-regular fa-folder-open"></i></div>
        <div class="text-box">
          <h3>My Documents</h3>
          <p>Upload & View Documents</p>
        </div>
      </div>
      <!-- 8: Digital ID Card (was 9) -->
      <div class="feature-card border-indigo" onclick="openIdCardModal()" style="cursor:pointer; animation-delay: 0.45s;">
        <div class="icon-box" style="background:#e0e7ff; color:#4f46e5;"><i class="fa-solid fa-id-badge"></i></div>
        <div class="text-box">
          <h3>Digital ID Card</h3>
          <p class="text-indigo">View & Print</p>
        </div>
      </div>
      <!-- 9: My Progress (was 11) -->
      <div class="feature-card border-indigo" onclick="openProgressModal()" style="cursor:pointer; animation-delay: 0.5s;">
        <div class="icon-box bg-indigo-light text-indigo" style="background:#e0e7ff; color:#4f46e5;"><i class="fa-solid fa-chart-line"></i></div>
        <div class="text-box">
          <h3>My Progress</h3>
          <p class="text-indigo">View Performance</p>
        </div>
      </div>
      <!-- 10: Apply Leave (was 4, locked) -->
      <div class="feature-card locked-card" style="animation-delay: 0.55s;">
        <div class="icon-box bg-gray-light text-gray"><i class="fa-regular fa-calendar-plus"></i></div>
        <div class="text-box">
          <h3>Apply Leave</h3>
          <p class="text-red">Coming Soon</p>
        </div>
        <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
      </div>
      <!-- 11: Fee Record (was 10, locked) -->
      <div class="feature-card locked-card" style="animation-delay: 0.6s;">
        <div class="icon-box bg-gray-light text-gray"><i class="fa-solid fa-indian-rupee-sign"></i></div>
        <div class="text-box">
          <h3>Fee Record</h3>
          <p class="text-red">Coming Soon</p>
        </div>
        <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
      </div>
      <!-- 12: School Gallery (was 12, locked) -->
      <div class="feature-card locked-card" style="animation-delay: 0.65s;">
        <div class="icon-box bg-gray-light text-gray"><i class="fa-solid fa-images"></i></div>
        <div class="text-box">
          <h3>School Gallery</h3>
          <p class="text-red">Coming Soon</p>
        </div>
        <div class="lock-icon"><i class="fa-solid fa-lock"></i></div>
      </div>
    </div>"""

# Find the start and end of erp-features-grid
start_idx = dash_html.find('<div class="erp-features-grid">')
end_idx = dash_html.find('</div>\n\n  <!-- Generic Dashboard Modal -->', start_idx)

if start_idx != -1 and end_idx != -1:
    dash_html = dash_html[:start_idx] + new_grid + dash_html[end_idx:]
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dash_html)
    print("Updated erp-dashboard.html cards order.")

# 2. Update js/erp-student.js
student_js_path = os.path.join(base_path, "js", "erp-student.js")
with open(student_js_path, "r", encoding="utf-8") as f:
    student_js = f.read()

student_js = student_js.replace("selector: '.feature-card:nth-child(4)',\n    title: 'Apply Leave',", "selector: '.feature-card:nth-child(10)',\n    title: 'Apply Leave',")
student_js = student_js.replace("selector: '.feature-card:nth-child(6)',\n    title: 'Daily Timetable',", "selector: '.feature-card:nth-child(5)',\n    title: 'Daily Timetable',")
student_js = student_js.replace("selector: '.feature-card:nth-child(7)',\n    title: 'Assignments',", "selector: '.feature-card:nth-child(6)',\n    title: 'Assignments',")
student_js = student_js.replace("selector: '.feature-card:nth-child(8)',\n    title: 'My Documents',", "selector: '.feature-card:nth-child(7)',\n    title: 'My Documents',")

with open(student_js_path, "w", encoding="utf-8") as f:
    f.write(student_js)
print("Updated js/erp-student.js selectors.")

# 3. Update js/main.js for Quick Call Back
main_js_path = os.path.join(base_path, "js", "main.js")
with open(main_js_path, "r", encoding="utf-8") as f:
    main_js = f.read()

old_qc_logic = """  setTimeout(() => {
    // Inject Modal HTML
    const modalHTML = `
      <div id="quick-callback-modal">
        <div class="qc-modal-content">
          <button class="qc-close" id="qc-close-btn"><i class="fa-solid fa-xmark"></i></button>
          
          <div class="qc-left">
            <div class="qc-left-content">
              <h3>Admissions Open 2026-27</h3>
              <p>Secure your child's future at Gurudev International Public School.</p>
              <ul>
                <li><i class="fa-solid fa-check"></i> Experienced Faculty</li>
                <li><i class="fa-solid fa-check"></i> Modern Infrastructure</li>
                <li><i class="fa-solid fa-check"></i> Holistic Development</li>
              </ul>
            </div>
          </div>
          
          <div class="qc-right">
            <div class="qc-header">
              <h4>Admission Support</h4>
              <h2>Get A Quick Call Back</h2>
              <p>Fill details for course guidance, scholarship, and fees.</p>
            </div>"""

new_qc_logic = """  if (!sessionStorage.getItem('quickCallbackShown')) {
  setTimeout(() => {
    // Inject Modal HTML
    const modalHTML = `
      <div id="quick-callback-modal">
        <div class="qc-modal-content" style="border-radius:24px; overflow:hidden;">
          <button class="qc-close" id="qc-close-btn" style="background:#fff; color:#333; box-shadow:0 4px 10px rgba(0,0,0,0.1);"><i class="fa-solid fa-xmark"></i></button>
          
          <div class="qc-left" style="background: linear-gradient(135deg, #1d4ed8, #1e3a8a); position:relative; overflow:hidden;">
            <div style="position:absolute; top:-50px; left:-50px; width:150px; height:150px; background:rgba(255,255,255,0.1); border-radius:50%;"></div>
            <div style="position:absolute; bottom:-30px; right:-30px; width:100px; height:100px; background:rgba(255,255,255,0.1); border-radius:50%;"></div>
            <div class="qc-left-content" style="position:relative; z-index:2;">
              <div style="font-size:2rem; margin-bottom:15px; color:#facc15;"><i class="fa-solid fa-graduation-cap"></i></div>
              <h3>Admissions Open 2026-27</h3>
              <p>Secure your child's future at Gurudev International Public School.</p>
              <ul style="margin-top:20px;">
                <li style="margin-bottom:10px;"><i class="fa-solid fa-check-circle" style="color:#facc15;"></i> Experienced Faculty</li>
                <li style="margin-bottom:10px;"><i class="fa-solid fa-check-circle" style="color:#facc15;"></i> Modern Infrastructure</li>
                <li><i class="fa-solid fa-check-circle" style="color:#facc15;"></i> Holistic Development</li>
              </ul>
            </div>
          </div>
          
          <div class="qc-right">
            <div class="qc-header">
              <h4 style="color:#2563eb; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Admissions Helpdesk</h4>
              <h2 style="font-weight:800; color:#0f172a;">Let's Connect!</h2>
              <p>Fill out the details below and our team will guide you through the process.</p>
            </div>"""

if "<h4>Admission Support</h4>" in main_js:
    main_js = main_js.replace(old_qc_logic, new_qc_logic)
    
    # We also need to add the closing brace for the `if (!sessionStorage...) {` statement
    # The timeout ends at: `}, 2000); // 2-second delay`
    
    end_pattern = "}, 2000); // 2-second delay"
    new_end_pattern = "sessionStorage.setItem('quickCallbackShown', 'true');\n    }, 2000); // 2-second delay\n  }"
    main_js = main_js.replace(end_pattern, new_end_pattern)
    
    with open(main_js_path, "w", encoding="utf-8") as f:
        f.write(main_js)
    print("Updated js/main.js for Quick Call Back logic.")
else:
    print("Could not find the Admission Support text in js/main.js.")
