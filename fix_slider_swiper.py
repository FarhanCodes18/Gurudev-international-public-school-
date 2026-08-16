import re

# 1. Update index.html
html_path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

new_html_block = """      <div id="achievers-slider-container-main" style="position:relative; max-width:100%; max-width:1000px; margin: 20px auto; display:none; padding: 0 40px;">
        <div class="swiper achieversSwiper" style="width: 100%; padding-top: 30px; padding-bottom: 50px;">
          <div class="swiper-wrapper" id="achieversTrack">
            <!-- Placeholders -->
          </div>
          <div class="swiper-button-prev" style="color:var(--primary); left:0;"></div>
          <div class="swiper-button-next" style="color:var(--primary); right:0;"></div>
          <div class="swiper-pagination"></div>
        </div>
      </div>"""

# Replace the entire achievers-slider-container-main div
pattern = re.compile(r'<div id="achievers-slider-container-main"[^>]*>.*?</div>\s*</div>\s*</section>', re.DOTALL)
html = pattern.sub(new_html_block + '\n    </div>\n  </section>', html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update js/achievers-slider.js to use Swiper
js_path = r'd:\Gurudev international\Gurudev intenational\js\achievers-slider.js'
with open(js_path, 'w', encoding='utf-8') as f:
    f.write("""document.addEventListener('DOMContentLoaded', () => {
  const track = document.getElementById('achieversTrack');
  if (!track) return;

  // Function to create a slide HTML
  function createSlide(photoObj) {
    return `
      <div class="swiper-slide" style="width:300px; height:450px;">
        <div class="achiever-card" style="position:relative; width:100%; height:100%; background:#fdf6e3; border-radius:24px; box-shadow:0 10px 30px rgba(0,0,0,0.2); overflow:hidden; border: 2px solid #5c2c2c;">
          <img src="${photoObj.image}" style="position:absolute; width:100%; height:100%; object-fit:cover; object-position:top center; left:0; top:0; z-index:1;" alt="${photoObj.name}">
          <img src="assets/icons/gurudev_school-removebg-preview.png" style="position:absolute; top:12px; right:12px; width:45px; height:45px; border-radius:50%; border:2px solid #5c2c2c; background:radial-gradient(circle, rgba(15,23,42,1) 0%, rgba(15,23,42,0.8) 100%); z-index:3; box-shadow:0 4px 10px rgba(0,0,0,0.5); object-fit:contain; padding:3px;" alt="Logo">
          <div class="achiever-info" style="position:absolute; bottom:0; left:0; width:100%; box-sizing:border-box; padding:120px 20px 25px; text-align:center; background:linear-gradient(to top, rgba(15, 23, 42, 1) 0%, rgba(15, 23, 42, 0.85) 40%, transparent 100%); color:white; z-index:2; transition:all 0.5s ease;">
            <h3 style="font-size:1.4rem; margin-bottom:8px; font-weight:900; text-transform:uppercase; text-shadow: 2px 2px 5px rgba(0,0,0,0.8); line-height:1.2; letter-spacing:1px;">${photoObj.name}</h3>
            <p style="font-size:1.15rem; color:#dc2626; font-weight:800; margin:0; text-shadow: 1px 1px 3px rgba(0,0,0,0.5);">${photoObj.score}</p>
          </div>
        </div>
      </div>
    `;
  }

  // --- LIVE SYNC FROM ADMIN PANEL ---
  const liveGalleryData = localStorage.getItem('admin_achievers_gallery');
  let photos = [];
  
  if (liveGalleryData) {
    try { photos = JSON.parse(liveGalleryData); } catch(e) {}
  }
  
  if (photos.length > 0) {
    const comingSoonBlock = document.getElementById('achievers-coming-soon');
    const sliderContainer = document.getElementById('achievers-slider-container-main');
    if (comingSoonBlock) comingSoonBlock.style.display = 'none';
    if (sliderContainer) sliderContainer.style.display = 'block';
    
    // Clear track
    track.innerHTML = '';
    
    // Duplicate photos if less than 4 so that Swiper loop works smoothly
    let displayPhotos = [...photos];
    while(displayPhotos.length > 0 && displayPhotos.length < 5) {
        displayPhotos = displayPhotos.concat(photos);
    }
    
    // Append slides
    displayPhotos.forEach(photoObj => {
      track.innerHTML += createSlide(photoObj);
    });
  } else {
    // Generate placeholders
    track.innerHTML = '';
    for(let i=0; i<5; i++){
        track.innerHTML += createSlide({name: "Coming Soon", score: "Stay Tuned!", image: "assets/images/school_building_main.png"});
    }
    const sliderContainer = document.getElementById('achievers-slider-container-main');
    if (sliderContainer) sliderContainer.style.display = 'block';
  }

  // Initialize Swiper
  if (typeof Swiper !== 'undefined') {
    new Swiper('.achieversSwiper', {
      effect: 'coverflow',
      grabCursor: true,
      centeredSlides: true,
      slidesPerView: 'auto',
      loop: true,
      loopedSlides: 3,
      coverflowEffect: {
        rotate: 0,
        stretch: 50,
        depth: 200,
        modifier: 1.5,
        slideShadows: true,
      },
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: '.achieversSwiper .swiper-button-next',
        prevEl: '.achieversSwiper .swiper-button-prev',
      },
      pagination: {
        el: '.achieversSwiper .swiper-pagination',
        clickable: true,
      },
      on: {
        slideChangeTransitionStart: function () {
            // Hide info for all slides
            const allInfos = this.el.querySelectorAll('.achiever-info');
            allInfos.forEach(info => {
                info.style.opacity = '0';
                info.style.transform = 'translateY(20px)';
            });
            // Show info for active slide
            const activeSlide = this.slides[this.activeIndex];
            if(activeSlide) {
                const activeInfo = activeSlide.querySelector('.achiever-info');
                if(activeInfo) {
                    activeInfo.style.opacity = '1';
                    activeInfo.style.transform = 'translateY(0)';
                }
            }
        },
        init: function() {
            setTimeout(() => {
                const activeSlide = this.slides[this.activeIndex];
                if(activeSlide) {
                    const activeInfo = activeSlide.querySelector('.achiever-info');
                    if(activeInfo) {
                        activeInfo.style.opacity = '1';
                        activeInfo.style.transform = 'translateY(0)';
                    }
                }
            }, 100);
        }
      }
    });
  }
});
""")

print("Swiper integration applied successfully.")
