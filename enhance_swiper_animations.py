import os

path = r'd:\Gurudev international\Gurudev intenational\css\style.css'
with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

# Enhanced animations for the CSE Faculty Slider
advanced_css = """
/* ==========================================================================
   ADVANCED CSE SWIPER ANIMATIONS & RESPONSIVENESS
   ========================================================================== */

/* Enhanced slide transition */
.swiper-slide { 
  opacity: 0.3; 
  transform: scale(0.85) translateY(30px); 
  transition: opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1), transform 0.8s cubic-bezier(0.4, 0, 0.2, 1); 
  pointer-events: none;
}
.swiper-slide-visible { 
  opacity: 1; 
  transform: scale(1) translateY(0); 
  pointer-events: auto;
}

/* Staggered text reveal inside the card during sliding */
.swiper-slide .cse-faculty-img img { filter: grayscale(80%) blur(2px); transition: all 0.8s ease; }
.swiper-slide-visible .cse-faculty-img img { filter: grayscale(0%) blur(0); }

.swiper-slide .cse-faculty-info h3 { transform: translateY(20px); opacity: 0; transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.1s; }
.swiper-slide .cse-faculty-info .designation { transform: translateY(20px); opacity: 0; transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.2s; }
.swiper-slide .cse-faculty-info .specialization { transform: translateY(20px); opacity: 0; transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s; }

.swiper-slide-visible .cse-faculty-info h3,
.swiper-slide-visible .cse-faculty-info .designation,
.swiper-slide-visible .cse-faculty-info .specialization { transform: translateY(0); opacity: 1; }

/* Responsive adjustments */
@media (max-width: 768px) {
  .cseSwiper { padding: 20px 15px 50px 15px !important; }
  .cse-next, .cse-prev { width: 35px !important; height: 35px !important; }
  .cse-next i, .cse-prev i { font-size: 1rem; }
  .cse-prev { left: 5px !important; }
  .cse-next { right: 5px !important; }
  .cse-faculty-img { height: 220px; }
}
"""

if 'ADVANCED CSE SWIPER ANIMATIONS' not in css:
    with open(path, 'a', encoding='utf-8') as f:
        f.write('\n' + advanced_css)
    print("Injected advanced CSS animations into style.css")
else:
    print("Advanced animations already injected.")
