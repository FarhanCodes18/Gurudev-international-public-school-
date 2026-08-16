
erp_css = """
/* ============================================================
   ERP / ADMIN / STUDENT PORTAL — RESPONSIVE CSS
   Applied to: erp-login, erp-register, erp-dashboard,
               erp-admin, admin-login, gurudev-super,
               student-portal, examination-result, notice-board,
               e-library
   ============================================================ */

/* ── ERP AUTH PAGES (login / register) ── */
.erp-auth-page,
body[style*="flex"][style*="center"] {
  padding: 16px;
}
.erp-auth-card {
  width: 90%;
  max-width: 460px;
  padding: clamp(24px, 5vw, 40px);
}
.erp-auth-card.wide { max-width: 800px; }

.erp-form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

@media (max-width: 768px) {
  .erp-auth-card       { padding: 28px 20px; max-height: 95dvh; overflow-y: auto; }
  .erp-auth-card.wide  { max-width: 100%; }
  .erp-form-grid       { grid-template-columns: 1fr; gap: 14px; }
  .erp-auth-header h2  { font-size: 1.4rem; }
  .erp-auth-header p   { font-size: 0.85rem; }
}
@media (max-width: 480px) {
  .erp-auth-card       { padding: 20px 14px; width: 96%; }
  .erp-auth-header h2  { font-size: 1.2rem; }
}

/* ── ERP DASHBOARD ── */
.erp-top-nav {
  padding: clamp(10px, 2vw, 16px) clamp(16px, 4vw, 32px);
}
.erp-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}
.feature-card {
  border-radius: 16px;
  padding: 20px 16px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  display: flex;
  align-items: center;
  gap: 14px;
}
.feature-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.erp-profile-banner {
  border-radius: clamp(12px, 3vw, 24px);
  padding: clamp(20px, 4vw, 36px);
  display: flex;
  gap: clamp(16px, 3vw, 28px);
  flex-wrap: wrap;
  align-items: center;
}
.erp-profile-img-wrapper img {
  width: clamp(70px, 15vw, 110px);
  height: clamp(70px, 15vw, 110px);
  border-radius: 50%;
  object-fit: cover;
}
.erp-profile-info h1 { font-size: clamp(1.2rem, 4vw, 2rem); }

.erp-modal { width: min(94vw, 600px); max-height: 88vh; overflow-y: auto; }

@media (max-width: 768px) {
  .erp-top-nav > div { flex-wrap: wrap; gap: 10px; }
  .erp-top-nav h2    { font-size: 1rem; }
  .erp-features-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .erp-profile-banner { flex-direction: column; text-align: center; }
  .erp-profile-banner .badges-row { justify-content: center; flex-wrap: wrap; }
  .erp-modal { width: 96vw; }
  .erp-modal-header h3 { font-size: 1.1rem; }
}
@media (max-width: 480px) {
  .erp-features-grid  { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .feature-card       { padding: 14px 10px; flex-direction: column; text-align: center; gap: 8px; }
  .icon-box           { width: 40px !important; height: 40px !important; font-size: 1.1rem !important; }
  .text-box h3        { font-size: 0.85rem; }
  .text-box p         { font-size: 0.75rem; }
  .erp-profile-info h1 { font-size: 1.2rem; }
}

/* ── ERP ADMIN TABLE ── */
.admin-table-wrap,
.erp-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 8px; }
.admin-table { min-width: 600px; }

@media (max-width: 768px) {
  .admin-table th, .admin-table td { padding: 10px 12px; font-size: 0.82rem; }
}

/* ── SUPER ADMIN / GURUDEV-SUPER ── */
.admin-layout, .sa-layout {
  display: flex;
  min-height: 100vh;
}
.admin-sidebar, .sa-sidebar {
  width: 260px;
  flex-shrink: 0;
  transition: transform 0.3s ease, width 0.3s ease;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.admin-main, .sa-main {
  flex: 1;
  min-width: 0;
  overflow-x: hidden;
  padding: clamp(16px, 3vw, 32px);
}
.admin-stats-grid, .sa-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.mobile-sidebar-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 1.4rem;
  cursor: pointer;
  padding: 8px;
  color: inherit;
}

@media (max-width: 992px) {
  .admin-layout, .sa-layout { position: relative; }
  .admin-sidebar, .sa-sidebar {
    position: fixed;
    left: 0; top: 0;
    transform: translateX(-100%);
    z-index: 9999;
    height: 100dvh;
    width: min(280px, 80vw);
    box-shadow: 4px 0 20px rgba(0,0,0,0.2);
  }
  .admin-sidebar.open, .sa-sidebar.open { transform: translateX(0); }
  .admin-main, .sa-main { margin-left: 0 !important; }
  .mobile-sidebar-toggle { display: flex; align-items: center; }
  .admin-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 9998; display: none; }
  .admin-overlay.visible { display: block; }
}
@media (max-width: 768px) {
  .admin-stats-grid, .sa-stats-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
  .admin-topbar { padding: 12px 16px; }
}
@media (max-width: 480px) {
  .admin-stats-grid, .sa-stats-grid { grid-template-columns: 1fr 1fr; gap: 10px; }
  .admin-main, .sa-main { padding: 12px; }
  .stat-number { font-size: 1.6rem; }
}

/* ── ADMIN LOGIN (admin-login.html — standalone dark theme) ── */
.login-wrapper {
  width: 100%;
  max-width: 480px;
  padding: clamp(16px, 4vw, 24px);
  margin: 0 auto;
}
.login-card {
  border-radius: clamp(12px, 3vw, 24px);
  padding: clamp(24px, 5vw, 40px);
  width: 100%;
}
@media (max-width: 480px) {
  .login-wrapper { padding: 16px; }
  .login-card    { padding: 24px 16px; border-radius: 16px; }
}

/* ── STUDENT PORTAL ── */
.portal-hero { padding: clamp(60px, 10vw, 120px) 0 clamp(40px, 6vw, 80px); }
.portal-features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}
@media (max-width: 768px) {
  .portal-features-grid { grid-template-columns: repeat(2, 1fr); gap: 14px; }
}
@media (max-width: 480px) {
  .portal-features-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
}

/* ── EXAMINATION RESULT ── */
.result-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 clamp(12px, 3vw, 20px);
}
.marks-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
.marks-table { min-width: 480px; }

@media (max-width: 768px) {
  .result-card         { border-radius: 12px; }
  .result-header-info  { flex-direction: column; gap: 12px; }
  .result-footer       { flex-direction: column; gap: 12px; }
  .marks-table th, .marks-table td { padding: 10px 12px; font-size: 0.83rem; }
}
@media (max-width: 480px) {
  .result-marks-bar    { height: 8px; }
  .result-grade        { font-size: 2rem; }
}

/* ── NOTICE BOARD ── */
.notice-list { display: flex; flex-direction: column; gap: 16px; }
.notice-card {
  border-radius: 12px;
  padding: clamp(16px, 3vw, 24px);
}
.notice-card-header { flex-wrap: wrap; gap: 10px; }

@media (max-width: 480px) {
  .notice-badge { font-size: 0.72rem; padding: 4px 8px; }
}

/* ── E-LIBRARY ── */
.elibrary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
@media (max-width: 600px) {
  .elibrary-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
}
@media (max-width: 380px) {
  .elibrary-grid { grid-template-columns: 1fr; }
}

/* ── MODALS on ERP pages ── */
.erp-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: none;
  place-items: center;
  z-index: 10000;
  padding: 16px;
}
.erp-modal-overlay.active { display: grid; }
.erp-modal {
  background: #fff;
  border-radius: 20px;
  width: min(94vw, 600px);
  max-height: 88dvh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}
.erp-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 1;
}
.erp-modal-body { padding: 20px 24px; }

@media (max-width: 480px) {
  .erp-modal-header { padding: 16px; }
  .erp-modal-body   { padding: 16px; }
  .erp-modal-header h3 { font-size: 1rem; }
}

/* ── CAREER APPLICATION FORM (print layout) ── */
@media (max-width: 768px) {
  .page { padding: 20px !important; }
  .field-row { flex-direction: column !important; gap: 12px !important; }
  .photo-box { width: 90px !important; height: 110px !important; }
  table { font-size: 11pt !important; }
  .sign-row { flex-direction: column; gap: 20px; }
}
@media print {
  body { padding: 0; font-size: 11pt; }
  .page { border: none; padding: 0; }
}

/* ── GLOBAL TABLE WRAPPER — ensure no page scrolls horizontally ── */
table {
  width: 100%;
  max-width: 100%;
}
.table-responsive,
.table-scroll-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  width: 100%;
}

/* ── GLOBAL CHART FIX ── */
canvas {
  max-width: 100% !important;
  height: auto !important;
}

/* ── INPUT FONT SIZE — prevent iOS auto-zoom ── */
@media (max-width: 768px) {
  input[type="text"],
  input[type="email"],
  input[type="password"],
  input[type="tel"],
  input[type="number"],
  input[type="search"],
  input[type="date"],
  select,
  textarea { font-size: 16px !important; }
}
"""

# Append to existing responsive.css
path = r'd:\Gurudev international\Gurudev intenational\css\responsive.css'
existing = open(path, encoding='utf-8').read()
if 'ERP / ADMIN / STUDENT PORTAL' not in existing:
    with open(path, 'a', encoding='utf-8') as f:
        f.write(erp_css)
    print("ERP/Admin responsive CSS appended!")
else:
    print("Already appended.")
