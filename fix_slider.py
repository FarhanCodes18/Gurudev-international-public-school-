import re

# Update index.html
html_path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Make placeholders 300x420, border-radius 20px, object-position top
html = html.replace('width:260px; height:380px;', 'width:300px; height:420px;')
html = html.replace('border-radius:16px;', 'border-radius:20px;')
html = html.replace('object-fit:cover;', 'object-fit:cover; object-position:top center; border-radius:20px;')

# Move arrows outwards and add some responsive protection
html = html.replace('id="achieverPrev" style="position:absolute; left:0;', 'id="achieverPrev" style="position:absolute; left:-10px;')
html = html.replace('id="achieverNext" style="position:absolute; right:0;', 'id="achieverNext" style="position:absolute; right:-10px;')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Update achievers-slider.js
js_path = r'd:\Gurudev international\Gurudev intenational\js\achievers-slider.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('width:260px; height:380px;', 'width:300px; height:420px;')
js = js.replace('border-radius:16px;', 'border-radius:20px;')
js = js.replace('object-fit:cover;', 'object-fit:cover; object-position:top center; border-radius:20px;')
js = js.replace('translateX = 180;', 'translateX = 220;')
js = js.replace('translateX = -180;', 'translateX = -220;')
js = js.replace('translateX = 320 +', 'translateX = 380 +')
js = js.replace('translateX = -320 -', 'translateX = -380 -')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated achievers styling.")
