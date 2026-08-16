import re

path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add foolproof script at the end of index.html
foolproof_script = """
    <!-- Explicit Swiper Initialization -->
    <script>
      document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
          if (typeof Swiper !== 'undefined' && document.querySelector('.cseSwiper')) {
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
        }, 500); // 500ms delay to ensure everything is loaded
      });
    </script>
  </body>
"""

if 'Explicit Swiper Initialization' not in content:
    content = content.replace('</body>', foolproof_script)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected explicit Swiper script into index.html")


# Fix CSS for the arrows so they are highly visible
css_path = r'd:\Gurudev international\Gurudev intenational\css\style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the old CSS for .cse-next, .cse-prev
old_css = """.cse-next, .cse-prev {
  color: var(--primary) !important;
  background: white; width: 50px !important; height: 50px !important; border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: 0.3s;
}"""

new_css = """.cseSwiper { position: relative; padding: 20px 40px 60px 40px !important; }
.cse-next, .cse-prev {
  color: white !important;
  background: var(--primary) !important; 
  width: 50px !important; height: 50px !important; 
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2); 
  transition: 0.3s;
  z-index: 100 !important;
}
.cse-prev { left: 0 !important; }
.cse-next { right: 0 !important; }
.cse-next:hover, .cse-prev:hover { background: var(--accent) !important; transform: scale(1.1); }
"""

if '.cseSwiper { position: relative; padding: 20px 40px 60px 40px !important; }' not in css:
    css = css.replace(old_css, new_css)
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("Fixed arrows CSS in style.css")
