import os
import glob

# Rename the files
try:
    if os.path.exists('d:/Gurudev international/Gurudev intenational/js/admin.js'):
        os.rename('d:/Gurudev international/Gurudev intenational/js/admin.js', 'd:/Gurudev international/Gurudev intenational/js/admin_v2.js')
    if os.path.exists('d:/Gurudev international/Gurudev intenational/js/main.js'):
        os.rename('d:/Gurudev international/Gurudev intenational/js/main.js', 'd:/Gurudev international/Gurudev intenational/js/main_v2.js')
    if os.path.exists('d:/Gurudev international/Gurudev intenational/js/gallery.js'):
        os.rename('d:/Gurudev international/Gurudev intenational/js/gallery.js', 'd:/Gurudev international/Gurudev intenational/js/gallery_v2.js')
except Exception as e:
    print(e)

# Update HTML files
html_files = glob.glob('d:/Gurudev international/Gurudev intenational/*.html')
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = content.replace('js/admin.js', 'js/admin_v2.js')
        content = content.replace('js/main.js', 'js/main_v2.js')
        content = content.replace('js/gallery.js', 'js/gallery_v2.js')
        
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {file}")
    except Exception as e:
        print(f"Skipped {file}: {e}")
