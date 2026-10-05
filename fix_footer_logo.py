import os
import glob
import re

html_files = glob.glob('*.html')
count = 0
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file, 'r', encoding='utf-16') as f:
            content = f.read()
    
    pattern = r'(<div\s+class=["\']footer-logo["\']\s*>)\s*(<img\s+[^>]*class=["\']footer-logo-image["\'][^>]*>)'
    
    def replacer(match):
        return f'{match.group(1)}\n<div class="footer-logo-emblem">\n{match.group(2)}\n</div>'
    
    new_content, num_subs = re.subn(pattern, replacer, content)
    
    if num_subs > 0:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Fixed footer logo in {file} ({num_subs} replacements)')
        count += 1

print(f"Total files fixed: {count}")
