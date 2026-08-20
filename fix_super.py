import re

with open('d:\\Gurudev international\\Gurudev intenational\\gurudev-super.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The original correct prefix up to the end of the sidebar
correct_prefix = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Superpower Admin Panel | GURUDEV ADMIN</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
  <link rel="stylesheet" href="css/admin.css" />
  <!-- Chart.js for Student Analytics -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="icon" type="image/png" href="assets/icons/gurudev_school-removebg-preview.png" />
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VT8PT9GZNW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VT8PT9GZNW');
</script>
<link rel="stylesheet" href="css/responsive.css" />
<script class="disable-inspect">document.addEventListener('contextmenu', e => e.preventDefault()); document.addEventListener('keydown', e => { if(e.key === 'F12' || (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) || (e.ctrlKey && e.key === 'U')) e.preventDefault(); });</script></head>
<body>
  
  <script>
    // Security check
    if(!sessionStorage.getItem('admin_session')) {
      window.location.href = 'admin-login.html';
    }
  </script>

  <!-- Loader Overlay for simulated actions -->
  <div class="admin-loader-overlay" id="admin-loader">
    <div class="admin-spinner"></div>
    <h3 id="loader-title" style="color:var(--admin-heading);">Processing...</h3>
    <p id="loader-desc" style="color:var(--admin-muted); font-size:0.9rem; margin-top:5px;">Please wait</p>
  </div>

  <!-- Mobile Sidebar Overlay -->
  <div class="admin-sidebar-overlay" id="admin-sidebar-overlay" onclick="closeSidebarMobile()"></div>

  <div class="admin-layout">
    
    <!-- SIDEBAR -->
    <aside class="admin-sidebar" id="admin-sidebar">
      <div class="sidebar-header">
        <div class="sidebar-logo">
          <img src="assets/icons/gurudev_school-removebg-preview.png" alt="Logo" class="sidebar-logo-img" />
        </div>
        <div>
          <div class="sidebar-title">Superpower Panel</div>
          <div class="sidebar-subtitle">GURUDEV ADMIN</div>
        </div>
      </div>
      
      <div class="sidebar-nav">
        <!-- 12 Modules -->
        <a class="nav-item active" data-view="dashboard"><i class="fa-solid fa-wallet"></i> Fees Portal</a>
        <a class="nav-item" data-view="academics"><i class="fa-solid fa-book-open"></i> Timetable & Assignments</a>
        <a class="nav-item" data-view="attendance"><i class="fa-solid fa-users-gear"></i> Attendance & Staff</a>
        <a class="nav-item" data-view="website"><i class="fa-solid fa-desktop"></i> Website Display</a>
        <a class="nav-item" data-view="notices"><i class="fa-solid fa-bullhorn"></i> Notices & E-Library</a>
        <a class="nav-item" data-view="calendar"><i class="fa-solid fa-calendar-days"></i> School Calendar</a>
        <a class="nav-item" data-view="admissions"><i class="fa-solid fa-file-signature"></i> Admissions & Callbacks</a>
        <a class="nav-item" data-view="results"><i class="fa-solid fa-square-poll-vertical"></i> Results & Reviews</a>
        <a class="nav-item" data-view="complaints"><i class="fa-solid fa-triangle-exclamation"></i> Complaint Queries</a>
        <a class="nav-item" data-view="reviews"><i class="fa-solid fa-star"></i> Student Reviews</a>
        <a class="nav-item" data-view="students"><i class="fa-solid fa-user-group"></i> Registered Students</a>
        <a class="nav-item" data-view="sms"><i class="fa-solid fa-comment-sms"></i> Bulk SMS Blaster</a>
        <a class="nav-item" data-view="documents"><i class="fa-solid fa-folder-open"></i> Student Documents</a>
        <a class="nav-item" data-view="analytics"><i class="fa-solid fa-chart-line"></i> Student Analytics</a>
        <a class="nav-item" data-view="certificate"><i class="fa-solid fa-award"></i> Certificate Maker</a>
        <a class="nav-item" data-view="transport"><i class="fa-solid fa-bus"></i> Transport Routes</a>
        <a class="nav-item" data-view="faculty"><i class="fa-solid fa-chalkboard-user"></i> Faculty Manager</a>
        <a class="nav-item" data-view="birthdays"><i class="fa-solid fa-cake-candles"></i> Student Birthdays</a>
      </div>
      
      <div style="padding: 20px; border-top: 1px solid var(--admin-border);">
        <button onclick="sessionStorage.removeItem('admin_session'); window.location.href='admin-login.html'" class="btn-admin-outline" style="width:100%; border-color:var(--admin-danger); color:var(--admin-danger);"><i class="fa-solid fa-arrow-right-from-bracket"></i> Logout</button>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="admin-main">
      <!-- HEADER -->
      <header class="admin-header">
        <div style="display:flex; align-items:center; gap:14px;">
          <button class="admin-sidebar-toggle" id="admin-sidebar-toggle" onclick="toggleSidebarMobile()" aria-label="Toggle Sidebar">
            <i class="fa-solid fa-bars"></i>
          </button>
"""

# Find the point where it should continue
match = re.search(r'          <div class="header-search">', content)
if match:
    idx = match.start()
    fixed_content = correct_prefix + content[idx:]
    with open('d:\\Gurudev international\\Gurudev intenational\\gurudev-super.html', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    print("Fixed!")
else:
    print("Could not find resume point")
