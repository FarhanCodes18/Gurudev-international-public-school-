import re
import os

filepath = r'd:\Gurudev international\Gurudev intenational\career.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace inline grids
content = content.replace(
    'class="career-process-grid" style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-top: 56px; position: relative;"',
    'class="career-process-grid" style="margin-top: 56px; position: relative;"'
)

content = content.replace(
    'class="career-apply-grid" style="display:grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 60px; align-items: start;"',
    'class="career-apply-grid" style="margin-top: 60px; align-items: start;"'
)

# Replace inline connector style (hide on mobile)
content = content.replace(
    'class="career-step-connector" style="position:absolute; top:48px; left:calc(12.5% + 24px); right:calc(12.5% + 24px); height:2px; background: linear-gradient(90deg, var(--primary), var(--accent)); z-index:0; opacity:0.3;"',
    'class="career-step-connector"'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated inline styles in career.html")

# Append base styles to style.css
css_additions = """
/* Career Section Base Grids */
.career-process-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }
.career-apply-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.career-step-connector { position: absolute; top: 48px; left: calc(12.5% + 24px); right: calc(12.5% + 24px); height: 2px; background: linear-gradient(90deg, var(--primary), var(--accent)); z-index: 0; opacity: 0.3; }
"""

style_path = r'd:\Gurudev international\Gurudev intenational\css\style.css'
with open(style_path, 'a', encoding='utf-8') as f:
    f.write(css_additions)
print("Added base grid styles to style.css")
