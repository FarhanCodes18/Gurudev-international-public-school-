import os
import glob

html_files = glob.glob('*.html')
count = 0
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file, 'r', encoding='utf-16') as f:
            content = f.read()
            
    if 'style.css?v=2.3' in content:
        content = content.replace('style.css?v=2.3', 'style.css?v=2.4')
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Cache busted in {file}')
        count += 1
    elif 'style.css' in content and 'style.css?' not in content:
        # if it doesn't have a version parameter, let's add one
        content = content.replace('"css/style.css"', '"css/style.css?v=2.4"')
        content = content.replace("'css/style.css'", "'css/style.css?v=2.4'")
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Cache version added in {file}')
        count += 1

print(f"Total files updated: {count}")
