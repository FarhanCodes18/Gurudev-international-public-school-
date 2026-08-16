import re

path = r'd:\Gurudev international\Gurudev intenational\css\responsive.css'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Hide the Apply Now button in navbar on mobile
# Find: .navbar-actions .btn-nav-primary { display: flex !important;
content = content.replace(
    '.navbar-actions .btn-nav-primary { display: flex !important;',
    '.navbar-actions .btn-nav-primary { display: none !important;'
)

# 2. Fix the hero stats grid overflowing on mobile by making the container fully responsive
# We'll inject a fix into the 768px and 480px media queries

fix_768 = """
  .hero-stats-grid { width: 100%; gap: 0; }
  .hero-stat { padding: 12px 10px; }
"""
if '.hero-stats-grid { width: 100%;' not in content:
    content = content.replace('  .hero-stats   { bottom: 16px; }', '  .hero-stats   { bottom: 16px; }\n' + fix_768)

fix_480 = """
  .hero-title { font-size: 1.6rem !important; word-wrap: break-word; }
  .hero-title .highlight { display: inline-block; max-width: 100%; overflow: hidden; text-overflow: ellipsis; }
  .hero-stats-grid { grid-template-columns: 1fr 1fr; border-radius: 12px; }
  .hero-stat { padding: 8px 4px; }
  .hero-stat-number { font-size: 1.15rem; }
  .hero-stat-label { font-size: 0.7rem; }
"""
if '.hero-title { font-size: 1.6rem' not in content:
    content = content.replace('  .hero-stat-number { font-size: 1.3rem; }', fix_480)


with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated responsive.css for top button and hero section")
