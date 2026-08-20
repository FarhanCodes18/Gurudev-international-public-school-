import glob

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
        except:
            continue

    original = content

    # Replace stat counter targets with single quotes
    content = content.replace("data-target='200'", "data-target='45'")
    content = content.replace(">200+</div>", ">45+</div>")
    content = content.replace(">200+<", ">45+<")
    
    # Replace single quoted text cases if any
    content = content.replace("200+ dedicated educators", "45+ expert faculty")
    content = content.replace("Over 200 dedicated educators", "Over 45 expert faculty")
    content = content.replace("team of 200+ educators", "team of 45+ expert faculty")
    
    # Check faculty.html specifically
    # Faculty Members -> Expert Faculty ?
    if file == 'faculty.html':
        content = content.replace("Faculty Members", "Expert Faculty")

    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated {file}")

print(f"Done. Updated {count} files.")
