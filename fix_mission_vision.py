import re
import os

path = r'd:\Gurudev international\Gurudev intenational\mission-vision.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace main grid inline styles
content = content.replace(
    'style="display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center"',
    'class="mv-main-grid"'
)

# Replace sub grid inline styles
content = content.replace(
    'class="why-grid" style="grid-template-columns:1fr 1fr;gap:16px;margin-top:24px"',
    'class="why-grid mv-sub-grid"'
)

# Add the style block
style_block = """
<style>
  .mv-main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
  .mv-sub-grid { grid-template-columns: 1fr 1fr !important; gap: 16px; margin-top: 24px; }
  @media (max-width: 992px) {
    .mv-main-grid { grid-template-columns: 1fr; gap: 40px; }
  }
  @media (max-width: 768px) {
    .mv-sub-grid { grid-template-columns: 1fr !important; }
  }
</style>
</head>
"""

if '.mv-main-grid {' not in content:
    content = content.replace('</head>', style_block)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("mission-vision.html inline grids have been replaced with responsive classes!")
