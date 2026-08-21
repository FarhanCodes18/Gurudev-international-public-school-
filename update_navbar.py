import os
import glob
import shutil
import re

# Files to process
html_files = glob.glob(r"d:\Gurudev international\Gurudev intenational\*.html")

replacements = {
    '<a href="principal-message.html" class="drawer-submenu-link"><i class="fa-solid fa-angle-right"></i> Principal\'s Message</a>': '<a href="management-committee.html" class="drawer-submenu-link"><i class="fa-solid fa-angle-right"></i> Management Committee</a>\n          <a href="principal-message.html" class="drawer-submenu-link"><i class="fa-solid fa-angle-right"></i> Principal\'s Message</a>',
    '<li><a href="principal-message.html">Principal\'s Message</a></li>': '<li><a href="management-committee.html">Management Committee</a></li>\n                                <li><a href="principal-message.html">Principal\'s Message</a></li>'
}

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        continue
        
    modified = False
    
    # Simple string replacements
    for old, new in replacements.items():
        if old in content and new not in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {os.path.basename(filepath)}")

print("Done updating navbar!")
