import glob
import os

html_files = glob.glob("*.html")
count = 0

for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

    original = content

    # Replace stat counter targets
    content = content.replace('data-target="200"', 'data-target="45"')
    content = content.replace('>200+</div>', '>45+</div>')
    
    # Replace labels from Expert Educators to Expert Faculty
    content = content.replace('Expert Educators', 'Expert Faculty')
    
    # Replace text occurrences
    content = content.replace('200+ dedicated educators', '45+ expert faculty')
    content = content.replace('Over 200 dedicated educators', 'Over 45 expert faculty')
    content = content.replace('team of 200+ educators', 'team of 45+ expert faculty')
    
    if content != original:
        # Determine encoding to write back
        # Just use utf-8 if possible, but keep original if read via latin-1?
        # Using utf-8 is usually safer for web files, let's write as utf-8
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated {file}")

print(f"Done. Updated {count} files.")
