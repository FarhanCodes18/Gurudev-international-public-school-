import codecs
import os

broken = '\u00e2\u20ac\u00ba'
fixed = '\u203a'

css_files = [
    'css/style.css',
    'css/animations.css',
    'css/responsive.css',
    'css/admin.css',
    'css/erp.css',
]

for filepath in css_files:
    if not os.path.exists(filepath):
        continue
    with codecs.open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if broken in content:
        content = content.replace(broken, fixed)
        with codecs.open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
    else:
        print(f"OK (no broken chars): {filepath}")
print("Done.")
