import re

with open('js/gallery.js', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("import('./firebase-config.js')", "import('./js/firebase-config.js')")
with open('js/gallery.js', 'w', encoding='utf-8') as f:
    f.write(content)

with open('js/admin.js', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("import('./firebase-config.js')", "import('./js/firebase-config.js')")
with open('js/admin.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed import paths")
