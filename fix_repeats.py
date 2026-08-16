import re

js_path = r'd:\Gurudev international\Gurudev intenational\js\achievers-slider.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Remove the cloning logic
js = re.sub(r'let displayPhotos = \[\.\.\.photos\];\s*while.*?\}\s*', 'let displayPhotos = [...photos];\n    ', js, flags=re.DOTALL)

# Change loop: true to dynamic loop based on displayPhotos.length
js = js.replace('loop: true,', 'loop: displayPhotos.length >= 3,')
js = js.replace('loopedSlides: 3,', 'loopedSlides: displayPhotos.length >= 3 ? 3 : null,')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Removed photo repeating.")
