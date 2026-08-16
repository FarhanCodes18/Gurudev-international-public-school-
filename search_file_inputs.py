import os
import glob

html_files = glob.glob('*.html')
for f in html_files:
    try:
        content = open(f, encoding='utf-8').read()
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'type="file"' in line:
                print(f"{f}:{i+1}: {line.strip()}")
    except:
        pass
