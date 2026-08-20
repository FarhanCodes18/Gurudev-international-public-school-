import glob

html_files = glob.glob("*.html")
snippet = """
<style>
  body {
    -webkit-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }
  input, textarea, select {
    -webkit-user-select: auto !important;
    -ms-user-select: auto !important;
    user-select: auto !important;
  }
</style>
<script class="disable-copy-paste">
  document.addEventListener('contextmenu', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    e.preventDefault();
  });
  document.addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    if (e.ctrlKey && ['c', 'C', 'v', 'V', 'x', 'X', 'a', 'A', 'u', 'U', 's', 'S', 'p', 'P'].includes(e.key)) {
      e.preventDefault();
    }
  });
  document.addEventListener('copy', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    e.preventDefault();
  });
  document.addEventListener('cut', e => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    e.preventDefault();
  });
</script>
</head>
"""

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
            
    if 'class="disable-copy-paste"' in content:
        continue
        
    original = content
    # Replace the last occurrence of </head> to be safe, or just normal replace
    content = content.replace("</head>", snippet)
    
    if content != original:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        print(f"Updated {file}")

print(f"Done. Updated {count} files.")
