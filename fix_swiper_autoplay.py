import re
import os

base = r'd:\Gurudev international\Gurudev intenational'
js_path = os.path.join(base, 'js', 'main.js')

with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

# I will replace the previously injected Swiper code with a more robust one that runs immediately if DOM is ready
# First, remove the old one:
old_code_pattern = r"// Executed outside or inside depending on scope\ndocument\.addEventListener\('DOMContentLoaded', function\(\) \{\n  // CSE Faculty Swiper Initialization.*\}\);\n"

# Remove old if it exists
new_content = re.sub(old_code_pattern, '', js_content, flags=re.DOTALL)

# Add the new robust code
better_code = """
// CSE Faculty Swiper Initialization
function initCSESwiper() {
  if (document.querySelector('.cseSwiper')) {
    new Swiper('.cseSwiper', {
      slidesPerView: 1,
      spaceBetween: 20,
      loop: true,
      speed: 800,
      watchSlidesProgress: true,
      autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: '.cse-next',
        prevEl: '.cse-prev',
      },
      breakpoints: {
        576: { slidesPerView: 2, spaceBetween: 20 },
        768: { slidesPerView: 3, spaceBetween: 30 },
        1024: { slidesPerView: 4, spaceBetween: 30 },
      }
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initCSESwiper);
} else {
  initCSESwiper();
}
"""

if 'initCSESwiper' not in new_content:
    new_content += "\n" + better_code

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated Swiper JS logic to fix autoplay.")
