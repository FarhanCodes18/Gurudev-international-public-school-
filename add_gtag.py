import os
import glob
import re

GTAG_SNIPPET = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-VT8PT9GZNW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-VT8PT9GZNW');
</script>"""

def add_gtag_to_files():
    html_files = glob.glob('*.html')
    modified_count = 0
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'G-VT8PT9GZNW' in content:
            print(f"Skipping {file_path}, already has gtag.")
            continue
            
        # Try to insert right after <head>
        match = re.search(r'<head.*?>', content, re.IGNORECASE)
        if match:
            pos = match.end()
            content = content[:pos] + '\n' + GTAG_SNIPPET + '\n' + content[pos:]
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            modified_count += 1
            print(f"Added gtag to {file_path}")
        else:
            print(f"Warning: Could not find <head> in {file_path}")
            
    print(f"Done. Modified {modified_count} files.")

if __name__ == '__main__':
    add_gtag_to_files()
