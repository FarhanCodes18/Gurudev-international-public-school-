import os
import re

base = r'd:\Gurudev international\Gurudev intenational'

# --- Add CSS ---
css_path = os.path.join(base, 'css', 'style.css')
with open(css_path, 'r', encoding='utf-8') as f:
    css_content = f.read()

cse_css = """
/* ==========================================================================
   CSE FACULTY SWIPER SECTION
   ========================================================================== */
.cse-section { overflow: hidden; }
.cseSwiper { padding: 20px 0 60px 0; }

.cse-faculty-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  transition: all 0.4s ease;
  height: 100%;
  position: relative;
  border: 1px solid rgba(0,0,0,0.03);
}

/* Faded animation for inactive slides */
.swiper-slide { opacity: 0.4; transition: opacity 0.6s ease, transform 0.6s ease; transform: scale(0.9); }
.swiper-slide-active, .swiper-slide-next, .swiper-slide-prev { opacity: 1; transform: scale(1); }
/* Actually, for 4 visible slides, we want all visible to be fully opaque if possible, 
   but Swiper assigns -active to the first visible one. 
   Let's just make all slides slightly faded on hover out, or just use Swiper's built-in transition. */
   
/* Let's redefine for a better look: */
.swiper-slide { opacity: 0.5; transform: scale(0.95) translateY(20px); transition: all 0.8s ease; }
.swiper-slide-visible { opacity: 1; transform: scale(1) translateY(0); }
.swiper-slide-active { opacity: 1; transform: scale(1) translateY(0); }

.cse-faculty-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.12); }

.cse-faculty-img { position: relative; overflow: hidden; height: 260px; }
.cse-faculty-img img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s ease; }
.cse-faculty-card:hover .cse-faculty-img img { transform: scale(1.1); }

.cse-faculty-overlay {
  position: absolute; inset: 0; background: linear-gradient(to top, rgba(11, 61, 145, 0.9), transparent);
  display: flex; align-items: flex-end; justify-content: center; gap: 15px;
  padding-bottom: 20px; opacity: 0; transition: all 0.4s ease;
}
.cse-faculty-card:hover .cse-faculty-overlay { opacity: 1; }
.cse-faculty-overlay a {
  width: 40px; height: 40px; background: white; color: var(--primary);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  text-decoration: none; font-size: 1.1rem; transition: 0.3s;
  transform: translateY(20px);
}
.cse-faculty-card:hover .cse-faculty-overlay a { transform: translateY(0); }
.cse-faculty-overlay a:hover { background: var(--accent); color: white; }
.cse-faculty-overlay a:nth-child(2) { transition-delay: 0.1s; }

.cse-faculty-info { padding: 24px; text-align: center; }
.cse-faculty-info h3 { font-size: 1.25rem; color: var(--text-dark); margin-bottom: 8px; font-weight: 700; }
.cse-faculty-info .designation { color: var(--primary); font-weight: 600; font-size: 0.9rem; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px; }
.cse-faculty-info .specialization { color: var(--text-secondary); font-size: 0.9rem; }

/* Swiper Controls */
.cse-next, .cse-prev {
  color: var(--primary) !important;
  background: white; width: 50px !important; height: 50px !important; border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1); transition: 0.3s;
}
.cse-next:hover, .cse-prev:hover { background: var(--primary); color: white !important; }
.cse-next::after, .cse-prev::after { font-size: 1.2rem !important; font-weight: 900; }
.swiper-pagination-bullet-active { background: var(--primary) !important; width: 25px !important; border-radius: 10px !important; }
"""

if 'CSE FACULTY SWIPER SECTION' not in css_content:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + cse_css)

# --- Add JS ---
js_path = os.path.join(base, 'js', 'main.js')
with open(js_path, 'r', encoding='utf-8') as f:
    js_content = f.read()

cse_js = """
  // CSE Faculty Swiper Initialization
  if (document.querySelector('.cseSwiper')) {
    new Swiper('.cseSwiper', {
      slidesPerView: 1,
      spaceBetween: 20,
      loop: true,
      watchSlidesProgress: true, // helps with .swiper-slide-visible
      autoplay: {
        delay: 2500,
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
"""

if 'CSE Faculty Swiper Initialization' not in js_content:
    # Insert before the end of DOMContentLoaded if it exists, or just append
    if '});' in js_content:
        # Find last closing brace of DOMContentLoaded
        # Simple append for now as main.js has multiple listeners or one main one
        js_content += "\n// Executed outside or inside depending on scope\ndocument.addEventListener('DOMContentLoaded', function() {" + cse_js + "});\n"
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

print("Injected CSS and JS logic for Swiper slider.")
