import os, glob, re

files = glob.glob('d:/Gurudev international/Gurudev intenational/*.html')
for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Increment v=number for main.js and admin.js
        new_content = re.sub(r'(js/(?:main|admin)\.js\?v=)(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 1), content)
        
        if new_content != content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated versions in {file}')
    except Exception as e:
        print(f"Skipping {file} due to error: {e}")
