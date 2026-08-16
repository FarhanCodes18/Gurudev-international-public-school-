import re

path = r'd:\Gurudev international\Gurudev intenational\css\responsive.css'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Hide hero-controls under 768px to prevent overlap
if '.hero-controls { display: none !important; }' not in content:
    content = content.replace(
        '.hero-controls { bottom: 64px; }',
        '.hero-controls { display: none !important; }'
    )

# Fix 2: Fix hero-stat-label text cut off under 480px
fix_label = """  .hero-stat-label { font-size: 0.65rem; letter-spacing: 0; word-wrap: break-word; white-space: normal; }"""
content = re.sub(r'  \.hero-stat-label \{ font-size: 0\.7rem; \}', fix_label, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed hero controls overlap and label truncation.")
