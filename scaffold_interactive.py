import os

base = r'd:\Gurudev international\Gurudev intenational'
html_files = ['science-lab.html', 'robotics-lab.html', 'library.html', 'sports.html']

# Create empty CSS and JS files if they don't exist
css_path = os.path.join(base, 'css', 'interactive.css')
js_path = os.path.join(base, 'js', 'interactive.js')

if not os.path.exists(css_path):
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write('/* Interactive Elements CSS */\n')
if not os.path.exists(js_path):
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write('/* Interactive Elements JS */\n')

# Inject links into the 4 HTML files
for file in html_files:
    filepath = os.path.join(base, file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changed = False
        # Inject CSS
        if 'css/interactive.css' not in content:
            content = content.replace('css/animations.css" />', 'css/animations.css" />\n  <link rel="stylesheet" href="css/interactive.css" />')
            changed = True
        
        # Inject JS
        if 'js/interactive.js' not in content:
            content = content.replace('<script src="js/animations.js"></script>', '<script src="js/animations.js"></script>\n  <script src="js/interactive.js"></script>')
            changed = True
            
        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Injected links into {file}")

print("Scaffolding complete.")
