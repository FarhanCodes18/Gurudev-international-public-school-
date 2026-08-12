import os
import re

workspace_dir = r"d:\Projects\Gurudev intenational"
index_path = os.path.join(workspace_dir, "index.html")

with open(index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

# Extract navbar-menu from index.html
nav_menu_match = re.search(r'<ul class="navbar-menu".*?</ul>', index_html, re.DOTALL)
if not nav_menu_match:
    print("Could not find navbar-menu in index.html")
    exit(1)
nav_menu_content = nav_menu_match.group(0)

# Extract drawer-nav from index.html
drawer_nav_match = re.search(r'<nav class="drawer-nav">.*?</nav>', index_html, re.DOTALL)
if not drawer_nav_match:
    print("Could not find drawer-nav in index.html")
    exit(1)
drawer_nav_content = drawer_nav_match.group(0)

# Replace in all other HTML files
count = 0
for filename in os.listdir(workspace_dir):
    if filename.endswith(".html") and filename != "index.html":
        filepath = os.path.join(workspace_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = re.sub(r'<ul class="navbar-menu".*?</ul>', nav_menu_content, content, flags=re.DOTALL)
        new_content = re.sub(r'<nav class="drawer-nav">.*?</nav>', drawer_nav_content, new_content, flags=re.DOTALL)
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Updated {filename}")

print(f"Successfully updated {count} HTML files.")
