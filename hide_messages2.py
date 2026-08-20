import glob
import os

html_files = ["d:/Gurudev international/Gurudev intenational/academics.html", "d:/Gurudev international/Gurudev intenational/career.html"]
count = 0

for file in html_files:
    try:
        with open(file, 'r', encoding='latin-1') as f:
            content = f.read()
        
        original = content
        
        # Remove existing if any
        content = content.replace('href="secretary-message.html" style="display: none !important;"', 'href="secretary-message.html"')
        content = content.replace('href="director-message.html" style="display: none !important;"', 'href="director-message.html"')
        
        # Add display:none to lock/hide them
        content = content.replace('href="secretary-message.html"', 'href="secretary-message.html" style="display: none !important;"')
        content = content.replace('href="director-message.html"', 'href="director-message.html" style="display: none !important;"')
        
        if content != original:
            with open(file, 'w', encoding='latin-1') as f:
                f.write(content)
            count += 1
            print(f"Updated {os.path.basename(file)}")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")

print(f"Done. Updated {count} files.")
