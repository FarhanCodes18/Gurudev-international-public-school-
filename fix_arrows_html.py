import os

path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Swiper arrows with explicit FontAwesome arrows
old_arrows = """        <!-- Navigation & Pagination -->
        <div class="swiper-pagination"></div>
        <div class="swiper-button-next cse-next"></div>
        <div class="swiper-button-prev cse-prev"></div>"""

new_arrows = """        <!-- Navigation & Pagination -->
        <div class="swiper-pagination"></div>
        <div class="cse-next"><i class="fa-solid fa-chevron-right"></i></div>
        <div class="cse-prev"><i class="fa-solid fa-chevron-left"></i></div>"""

if 'class="cse-next"' not in content:
    content = content.replace(old_arrows, new_arrows)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced arrows in index.html")
else:
    print("Arrows already replaced in index.html, or no match found")
