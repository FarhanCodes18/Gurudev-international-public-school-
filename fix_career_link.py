content = open('career.html', 'r', encoding='utf-8').read()

# Update the download link to point to HTML form (which users can print to PDF)
old = 'href="assets/downloads/career-application-form.pdf"'
new = 'href="assets/downloads/career-application-form.html" target="_blank"'
content = content.replace(old, new)

# Also update download attribute
old2 = 'download="Gurudev-Career-Application-Form.pdf"'
new2 = 'onclick="window.open(\'assets/downloads/career-application-form.html\'); return false;"'
content = content.replace(old2, new2)

open('career.html', 'w', encoding='utf-8').write(content)
print("Download link updated!")
