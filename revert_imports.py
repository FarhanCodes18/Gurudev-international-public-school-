import os
import glob

files = glob.glob('d:/Gurudev international/Gurudev intenational/js/*.js')
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    if "import('./js/firebase-config.js')" in content:
        content = content.replace("import('./js/firebase-config.js')", "import('./firebase-config.js')")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Reverted {file}')
