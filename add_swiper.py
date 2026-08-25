import sys

with open(r'd:\Gurudev international\Gurudev intenational\faculty.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add CSS
if 'swiper-bundle.min.css' not in text:
    text = text.replace('css/style.css?v=2.2', 'https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.css" />\n  <link rel="stylesheet" href="css/style.css?v=2.2')

# Add JS
if 'swiper-bundle.min.js' not in text:
    text = text.replace('js/loader.js', 'https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>\n  <script src="js/loader.js')

with open(r'd:\Gurudev international\Gurudev intenational\faculty.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added Swiper to faculty.html')
