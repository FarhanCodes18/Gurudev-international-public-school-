import os
import glob

html_files = glob.glob(r"d:\Gurudev international\Gurudev intenational\*.html")

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        continue
        
    if 'css/style.css' in content:
        # replace css/style.css with css/style.css?v=2.2 (or just append if not there)
        content = content.replace('css/style.css?v=2.1', 'css/style.css?v=2.2')
        content = content.replace('css/style.css"', 'css/style.css?v=2.2"')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
