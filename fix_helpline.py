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

    content = content.replace("tel:+919876500000", "tel:+917770822000")
    content = content.replace("Helpline: +91 98765 00000", "Helpline: 7770822000")
    content = content.replace(" | +91 98765 00000", "")
    content = content.replace("<br/>+91 98765 00000", "")
    content = content.replace("+91 98765 00000", "7770822000, 9753187666")

    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated {file}")

print(f"Done. Updated {count} files.")
