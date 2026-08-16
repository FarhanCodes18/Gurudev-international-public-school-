import re

# 1. Update style.css
css_path = r'd:\Gurudev international\Gurudev intenational\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(r'\.achiever-card\.active\s*\{\s*border-color:\s*#fde047;[^\}]+\}', '.achiever-card.active { box-shadow: 0 20px 40px rgba(0,0,0,0.5); }', css)
css = re.sub(r'border:\s*4px\s*solid\s*transparent;', 'border: none;', css)

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Update js/achievers-slider.js
js_path = r'd:\Gurudev international\Gurudev intenational\js\achievers-slider.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

new_js_card_generation = """
        const card = document.createElement('div');
        card.className = 'achiever-card';
        card.style.cssText = 'position:absolute; width:300px; height:450px; background:#fdf6e3; border-radius:24px; box-shadow:0 10px 30px rgba(0,0,0,0.2); overflow:hidden; transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); display:flex; flex-direction:column; border: 2px solid #5c2c2c;';
        card.innerHTML = `
          <img src="${photoObj.image}" style="position:absolute; width:100%; height:100%; object-fit:cover; object-position:top center; border-radius:24px; left:0; top:0; z-index:1;" alt="${photoObj.name}">
          <img src="assets/icons/gurudev_school-removebg-preview.png" style="position:absolute; top:12px; right:12px; width:45px; height:45px; border-radius:50%; border:2px solid #5c2c2c; background:radial-gradient(circle, rgba(15,23,42,1) 0%, rgba(15,23,42,0.8) 100%); z-index:3; box-shadow:0 4px 10px rgba(0,0,0,0.5); object-fit:contain; padding:3px;" alt="Logo">
          <div class="achiever-info" style="position:absolute; bottom:0; left:0; width:100%; box-sizing:border-box; padding:120px 20px 25px; text-align:center; background:linear-gradient(to top, rgba(15, 23, 42, 1) 0%, rgba(15, 23, 42, 0.85) 40%, transparent 100%); color:white; z-index:2; border-bottom-left-radius:24px; border-bottom-right-radius:24px; transition:all 0.5s ease;">
            <h3 style="font-size:1.4rem; margin-bottom:8px; font-weight:900; text-transform:uppercase; text-shadow: 2px 2px 5px rgba(0,0,0,0.8); line-height:1.2; letter-spacing:1px;">${photoObj.name}</h3>
            <p style="font-size:1.15rem; color:#dc2626; font-weight:800; margin:0; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">${photoObj.score}</p>
          </div>
        `;
        track.appendChild(card);
"""

# Replace the inner block of JS
# We will use regex to find the `livePhotos.forEach` block and replace it
pattern_js = re.compile(r'livePhotos\.forEach\(photoObj => \{.*?(?=^\s*\}\);) \}\);', re.DOTALL | re.MULTILINE)
# Since the regex might be tricky, let's use a simpler approach for JS
# We know it starts with `livePhotos.forEach(photoObj => {` and ends with `track.appendChild(card);`
start_marker = 'livePhotos.forEach(photoObj => {'
end_marker = 'track.appendChild(card);\n      });'

start_idx = js.find(start_marker)
end_idx = js.find(end_marker) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    js = js[:start_idx] + "livePhotos.forEach(photoObj => {" + new_js_card_generation + "      });" + js[end_idx:]
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js)
else:
    print("Failed to patch JS")

# 3. Update index.html
html_path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

new_placeholder = """          <div class="achiever-card" style="position:absolute; width:300px; height:450px; background:#fdf6e3; border-radius:24px; box-shadow:0 10px 30px rgba(0,0,0,0.2); overflow:hidden; transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); display:flex; flex-direction:column; border: 2px solid #5c2c2c;">
            <img src="assets/images/school_building_main.png" style="position:absolute; width:100%; height:100%; object-fit:cover; object-position:top center; border-radius:24px; left:0; top:0; z-index:1; filter:blur(8px) brightness(0.7);" alt="Student">
            <img src="assets/icons/gurudev_school-removebg-preview.png" style="position:absolute; top:12px; right:12px; width:45px; height:45px; border-radius:50%; border:2px solid #5c2c2c; background:radial-gradient(circle, rgba(15,23,42,1) 0%, rgba(15,23,42,0.8) 100%); z-index:3; box-shadow:0 4px 10px rgba(0,0,0,0.5); object-fit:contain; padding:3px;" alt="Logo">
            <div class="achiever-info" style="position:absolute; bottom:0; left:0; width:100%; box-sizing:border-box; padding:120px 20px 25px; text-align:center; background:linear-gradient(to top, rgba(15, 23, 42, 1) 0%, rgba(15, 23, 42, 0.85) 40%, transparent 100%); color:white; z-index:2; border-bottom-left-radius:24px; border-bottom-right-radius:24px; opacity:0; transform:translateY(20px); transition:all 0.5s ease;">
              <h3 style="font-size:1.4rem; margin-bottom:8px; font-weight:900; text-transform:uppercase; text-shadow: 2px 2px 5px rgba(0,0,0,0.8); line-height:1.2; letter-spacing:1px;">Coming Soon</h3>
              <p style="font-size:1.15rem; color:#dc2626; font-weight:800; margin:0; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">Stay Tuned!</p>
            </div>
          </div>"""

# Replace all 5 placeholders in index.html
# Find the start of the cards and end
start_marker = '<!-- 5 Placeholder Cards (Will be populated by admin) -->'
end_marker = '</div>\n        \n        <!-- Controls -->'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_html_block = start_marker + '\n' + (new_placeholder + '\n') * 5 + '        '
    html = html[:start_idx] + new_html_block + html[end_idx:]
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
else:
    print("Failed to patch HTML")

print("All updates complete!")
