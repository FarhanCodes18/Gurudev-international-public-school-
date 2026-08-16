import sys
sys.stdout.reconfigure(encoding='utf-8')

css = r"""/* ============================================================
   GURUDEV INTERNATIONAL -- COMPLETE RESPONSIVE CSS OVERHAUL
   Mobile-First | 320px to 1920px+
   ============================================================ */

/* GLOBAL RESET */
*, *::before, *::after { box-sizing: border-box; }
html { overflow-x: hidden; scroll-behavior: smooth; }
body { overflow-x: hidden; max-width: 100vw; -webkit-text-size-adjust: 100%; }
img, video, iframe, canvas, svg { max-width: 100%; height: auto; display: block; }

/* CONTAINER */
.container {
  width: 100%;
  max-width: var(--container-width, 1280px);
  margin: 0 auto;
  padding: 0 clamp(16px, 4vw, 40px);
}

/* FLUID TYPOGRAPHY */
h1, .hero-title      { font-size: clamp(1.8rem, 5vw, 4rem); line-height: 1.15; }
h2, .section-title   { font-size: clamp(1.4rem, 3.5vw, 2.8rem); line-height: 1.2; }
h3                   { font-size: clamp(1.05rem, 2.5vw, 1.6rem); }
h4                   { font-size: clamp(0.95rem, 2vw, 1.3rem); }
.section-subtitle    { font-size: clamp(0.88rem, 1.8vw, 1.1rem); }
.page-hero-title     { font-size: clamp(1.5rem, 5vw, 3rem); }

/* SECTION PADDING */
.section-padding    { padding: clamp(40px, 8vw, 100px) 0; }
.section-padding-sm { padding: clamp(24px, 5vw, 60px) 0; }

/* ============================================================
   1440px -- LARGE DESKTOP
   ============================================================ */
@media (max-width: 1440px) {
  :root { --container-width: 1200px; }
}

/* ============================================================
   1200px -- DESKTOP
   ============================================================ */
@media (max-width: 1200px) {
  :root { --container-width: 960px; }
  .footer-grid { grid-template-columns: 1.5fr 1fr 1fr 1fr; gap: 36px; }
  .mega-menu   { min-width: 540px; }
  .facilities-grid { grid-template-columns: repeat(3, 1fr); }
  .toppers-grid    { grid-template-columns: repeat(4, 1fr); }
}

/* ============================================================
   992px -- TABLET LANDSCAPE
   ============================================================ */
@media (max-width: 992px) {
  :root { --container-width: 100%; --section-padding: 70px 0; }

  .navbar-menu { display: none !important; }
  .hamburger   { display: flex !important; }
  .navbar-actions .btn-nav-outline { display: none; }
  .contact-header { display: none; }
  .mega-menu { min-width: 260px; }
  .mega-menu-grid { grid-template-columns: 1fr; }

  .hero-stats-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-arrows     { display: none; }

  .about-content     { grid-template-columns: 1fr; gap: 40px; }
  .about-image-block { max-width: 560px; margin: 0 auto; }

  .grid-2 { grid-template-columns: 1fr; }
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }

  .stats-grid      { grid-template-columns: repeat(2, 1fr); }
  .messages-grid   { grid-template-columns: 1fr; max-width: 500px; margin: 0 auto; }
  .facilities-grid { grid-template-columns: repeat(2, 1fr); }
  .why-grid        { grid-template-columns: repeat(2, 1fr); }
  .testimonial-card { min-width: calc(50% - 12px); }
  .news-grid       { grid-template-columns: repeat(2, 1fr); }
  .gallery-grid    { grid-template-columns: repeat(3, 1fr); }
  .gallery-item.large, .gallery-item.wide { grid-column: span 1; grid-row: span 1; }
  .toppers-grid    { grid-template-columns: repeat(3, 1fr); }

  .footer-grid  { grid-template-columns: 1fr 1fr; gap: 32px; }
  .footer-brand { grid-column: span 2; }

  .contact-form-wrapper { grid-template-columns: 1fr; gap: 40px; }
  .admission-content { flex-direction: column; text-align: center; }
  .admission-actions { justify-content: center; }

  .timeline::before { left: 20px; }
  .timeline-item,
  .timeline-item:nth-child(even) {
    justify-content: flex-start;
    padding-right: 0;
    padding-left: 60px;
    transform: translateX(0);
  }
  .timeline-dot { left: 20px; }

  .video-wrapper { max-width: 700px; margin: 0 auto; }

  .faculty-card { flex: 0 0 calc(33.333% - 20px); }
  .faculty-slider-wrapper { padding: 0 50px; }

  .career-apply-grid    { grid-template-columns: 1fr; gap: 40px; }
  .career-process-grid  { grid-template-columns: repeat(2, 1fr); }
  .career-openings-grid { grid-template-columns: repeat(2, 1fr); }
}

/* ============================================================
   768px -- TABLET PORTRAIT
   ============================================================ */
@media (max-width: 768px) {
  :root { --section-padding: 60px 0; }

  html, body { overflow-x: hidden !important; max-width: 100vw; }

  .container { padding: 0 clamp(12px, 3vw, 20px); }

  .top-bar { padding: 7px 0; }
  .marquee-item { font-size: 0.75rem; padding: 0 18px; }

  .navbar-inner { height: 62px; }
  .logo-text    { display: none; }
  .logo-emblem  { width: 44px; height: 44px; }
  .navbar-actions .btn-nav { display: none; }
  .navbar-actions .btn-nav-primary { display: flex !important; font-size: 0.72rem; padding: 6px 14px; }

  .hero { height: 92vh; min-height: 560px; }
  .hero-text    { max-width: 100%; padding: 0; }
  .hero-subtitle { font-size: 0.92rem; }
  .hero-buttons  { flex-wrap: wrap; gap: 10px; }
  .hero-buttons .btn { font-size: 0.85rem; padding: 12px 20px; }
  .hero-stats   { bottom: 16px; }
  .hero-stat-number { font-size: 1.5rem; }
  .scroll-indicator { display: none; }
  .hero-controls { bottom: 64px; }

  .about-features     { grid-template-columns: 1fr; }
  .about-image-accent { display: none; }
  .about-image-badge  { left: 8px; bottom: 8px; }

  .section-header-flex { flex-direction: column; align-items: flex-start; gap: 14px; }

  .grid-3 { grid-template-columns: 1fr; }
  .grid-4 { grid-template-columns: 1fr 1fr; }
  .stats-grid      { grid-template-columns: repeat(2, 1fr); }
  .facilities-grid { grid-template-columns: repeat(2, 1fr); gap: 16px; }
  .why-grid        { grid-template-columns: 1fr; }
  .news-grid       { grid-template-columns: 1fr; max-width: 480px; margin: 0 auto; }
  .gallery-grid    { grid-template-columns: repeat(2, 1fr); grid-auto-rows: 150px; }
  .gallery-item.large, .gallery-item.wide, .gallery-item.tall { grid-column: span 1; grid-row: span 1; }
  .toppers-grid    { grid-template-columns: repeat(2, 1fr); }
  .messages-grid   { max-width: 100%; }

  .testimonial-card { min-width: 100%; margin-right: 24px; }

  .form-row { grid-template-columns: 1fr; }
  .contact-form-card { padding: 24px 16px; }
  input[type="text"], input[type="email"], input[type="tel"],
  input[type="number"], input[type="password"], select, textarea { font-size: 16px !important; }

  .footer      { padding-bottom: 88px; }
  .footer-main { padding: 48px 0 28px; }
  .footer-grid { grid-template-columns: 1fr; gap: 0; }
  .footer-brand { grid-column: auto; padding-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 4px; }
  .footer-col   { border-bottom: 1px solid rgba(255,255,255,0.07); overflow: hidden; }
  .footer-col-title { padding: 14px 0; margin-bottom: 0; display: flex; justify-content: space-between; align-items: center; cursor: pointer; user-select: none; }
  .footer-col-title::after { content: '+'; font-size: 1.1rem; color: var(--accent, #d4af37); }
  .footer-col.open .footer-col-title::after { content: '-'; }
  .footer-links, .footer-contact-items-wrap { max-height: 0; overflow: hidden; transition: max-height 0.35s ease, padding 0.35s ease; padding-bottom: 0; }
  .footer-col.open .footer-links, .footer-col.open .footer-contact-items-wrap { max-height: 400px; padding-bottom: 16px; }
  .footer-bottom { flex-direction: column; gap: 10px; text-align: center; padding: 16px 0; }
  .footer-copyright { font-size: 0.76rem; }
  .footer-social    { gap: 12px; }
  .footer-social-icon { width: 42px; height: 42px; font-size: 0.95rem; }

  .timeline-item { flex-direction: column; padding-left: 56px; padding-right: 0; }
  .timeline-dot  { left: 16px; }
  .timeline::before { left: 16px; }

  .admission-content { flex-direction: column; text-align: center; gap: 20px; }
  .admission-actions { justify-content: center; flex-wrap: wrap; }
  .admission-actions .btn { width: 100%; max-width: 280px; }

  .disclosure-table-wrap, .marks-table-wrap, .table-scroll-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .disclosure-table, .marks-table { min-width: 480px; }
  .disclosure-table th, .disclosure-table td { padding: 10px 12px; font-size: 0.82rem; }

  .gallery-lightbox-content { width: 96% !important; max-height: 80vh !important; }
  .gallery-lightbox-close { top: 8px !important; right: 8px !important; }

  .result-card        { padding: 20px !important; }
  .result-header-info { flex-direction: column !important; gap: 12px !important; }
  .result-footer      { flex-direction: column !important; gap: 12px !important; }

  .faculty-card { flex: 0 0 calc(50% - 15px); }
  .faculty-slider-wrapper { padding: 0 40px; }
  .faculty-placeholder { height: 180px; }

  .career-process-grid  { grid-template-columns: 1fr; }
  .career-openings-grid { grid-template-columns: 1fr; }
  .career-apply-box { padding: 32px 20px; }
  .career-step-connector { display: none; }

  #bus-route-canvas { height: 200px !important; }
  .bm-info-panel { flex-direction: column; }
  .bm-stop-card, .bm-bus-status { min-width: 100%; }
  .bm-title { font-size: 1.6rem; }
  .bm-tabs  { gap: 6px; flex-wrap: wrap; }
  .bm-tab   { padding: 6px 14px; font-size: 0.78rem; }

  #lab-network-canvas { height: 220px !important; }
  .lm-info-panel { flex-direction: column; }
  .lm-node-card, .lm-network-status { min-width: 100%; }
  .lm-title   { font-size: 1.6rem; }
  .lm-metrics { grid-template-columns: 1fr 1fr; }

  .page-hero { padding: 80px 0 40px; }
  .page-hero-title  { font-size: clamp(1.4rem, 6vw, 2.2rem) !important; }
  .about-content    { grid-template-columns: 1fr !important; }
  .about-image-main img { height: 280px !important; }
  .services-grid    { grid-template-columns: 1fr !important; }
  .features-grid    { grid-template-columns: 1fr !important; }

  .admin-grid-4, .admin-grid-3 { grid-template-columns: repeat(2, 1fr) !important; }
  .admin-table-wrap { overflow-x: auto; }
  .admin-chart      { width: 100% !important; height: auto !important; }
}

/* ============================================================
   576px -- LARGE MOBILE
   ============================================================ */
@media (max-width: 576px) {
  .hero-buttons        { flex-direction: column; align-items: stretch; }
  .hero-buttons .btn   { width: 100%; text-align: center; justify-content: center; }
  .facilities-grid     { grid-template-columns: 1fr; }
  .gallery-grid        { grid-template-columns: 1fr; grid-auto-rows: 200px; }
  .faculty-card        { flex: 0 0 calc(50% - 15px); }
  .admission-actions .btn { width: 100%; max-width: 100%; }
}

/* ============================================================
   480px -- MOBILE
   ============================================================ */
@media (max-width: 480px) {
  :root { --section-padding: 50px 0; }

  .logo-image { width: 38px; height: 38px; }
  .hero { height: 100dvh; min-height: 520px; }
  .hero-stat { padding: 10px 8px; }
  .hero-stat-number { font-size: 1.3rem; }
  .hero-badge { font-size: 0.7rem; }

  .stats-grid  { grid-template-columns: 1fr 1fr; gap: 12px; }
  .stat-card   { padding: 20px 12px; border-radius: 12px; }
  .stat-number { font-size: 2rem; }
  .stat-icon   { width: 44px; height: 44px; font-size: 1.2rem; }

  .facilities-grid { grid-template-columns: 1fr; gap: 14px; }
  .facility-card   { height: 220px; }
  .why-card { padding: 24px 18px; }

  .message-card   { padding: 20px; }
  .message-avatar { width: 68px; height: 68px; }

  .faculty-card   { flex: 0 0 100%; }
  .faculty-slider-wrapper { padding: 0 30px; }
  .faculty-placeholder { height: 200px; }
  .faculty-name   { font-size: 1.1rem; }

  .career-process-step { padding: 24px 16px; }
  .career-step-number  { width: 48px; height: 48px; font-size: 1.1rem; }
  .career-opening-card { padding: 20px 16px; }
  .career-apply-box    { padding: 28px 16px; }
  .career-download-btn { flex-direction: column; text-align: center; width: 100%; }

  .erp-auth-card { padding: 24px 14px !important; width: 95%; }

  .about-image-main img { height: 220px !important; }

  #bus-route-canvas   { height: 160px !important; }
  .bm-title           { font-size: 1.3rem; }
  .bm-canvas-wrap     { padding: 12px; }
  #lab-network-canvas { height: 180px !important; }
  .lm-canvas-wrap     { padding: 12px; }

  .admin-grid-4, .admin-grid-3, .admin-grid-2 { grid-template-columns: 1fr !important; }

  .footer-logo-text .name { font-size: 0.8rem; }
  .footer-desc            { font-size: 0.82rem; }
  .footer-social-icon     { width: 40px; height: 40px; }
}

/* ============================================================
   375px -- SMALL MOBILE
   ============================================================ */
@media (max-width: 375px) {
  .container    { padding: 0 12px; }
  .hero-title   { font-size: 1.55rem; }
  .stats-grid   { gap: 10px; }
  .navbar-actions { gap: 8px; }
  .why-card-icon { width: 50px; height: 50px; }
}

/* TOUCH TARGETS */
@media (max-width: 1024px) {
  a, button, [role="button"], input[type="submit"], input[type="button"] { min-height: 44px; }
  .facility-link, .news-read-more, .message-read-more,
  .dropdown-item, .mega-menu-item, .drawer-nav-link { min-height: 44px; display: flex; align-items: center; }
}

/* CONSISTENT IMAGE COVERS */
.facility-card img,
.news-image img,
.gallery-item img,
.about-image-main img,
.hero-slide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* MOBILE DRAWER */
.mobile-drawer  { width: min(340px, 90vw) !important; }
.mobile-overlay { width: 100vw; height: 100vh; }

/* FOOTER LINK ARROW */
.footer-link::before { content: '\203a'; }

/* LARGE DESKTOP (1441px+) */
@media (min-width: 1441px) {
  :root { --container-width: 1320px; }
  .hero-title    { font-size: 4.2rem; }
  .section-title { font-size: 3rem; }
  .facilities-grid { grid-template-columns: repeat(4, 1fr); }
  .why-grid { grid-template-columns: repeat(3, 1fr); }
}

/* PRINT */
@media print {
  .navbar, .footer, .hero-arrows, .scroll-indicator,
  .floating-buttons, .hamburger, .top-bar { display: none !important; }
  body { font-size: 12pt; }
}
"""

with open(r'd:\Gurudev international\Gurudev intenational\css\responsive.css', 'w', encoding='utf-8') as f:
    f.write(css)
print("responsive.css written!")
