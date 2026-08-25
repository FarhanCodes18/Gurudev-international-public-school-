import os
import glob
import re

html_files = glob.glob(r'd:\Gurudev international\Gurudev intenational\*.html')
count = 0

for file_path in html_files:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Using simple replace for the exact string first, then regex for variations
    exact_str = '<a href="faculty.html"  class="dropdown-item"><i class="fa-solid fa-chalkboard-teacher"></i> Our Faculty</a>'
    
    if exact_str in content or re.search(r'<a href="faculty\.html"\s*class="dropdown-item">\s*<i class="fa-solid fa-chalkboard-teacher"></i>\s*Our Faculty</a>', content):
        new_content = re.sub(r'[ \t]*<a href="faculty\.html"\s*class="dropdown-item">\s*<i class="fa-solid fa-chalkboard-teacher"></i>\s*Our Faculty</a>[ \t]*\n?', '', content)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception:
            with open(file_path, 'w', encoding='latin-1') as f:
                f.write(new_content)
        
        count += 1
        print(f'Updated {os.path.basename(file_path)}')

print(f'Done updating {count} files.')
