import re

# 1. Update index.html
html_path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

new_html_block = """      <div id="achievers-slider-container-main" style="position:relative; max-width:100%; max-width:900px; margin: 40px auto; display:none; padding: 0 60px;">
        <div class="swiper-button-prev achiever-prev" style="color:var(--primary); left:10px; width:50px; height:50px; background:white; border-radius:50%; box-shadow:0 4px 10px rgba(0,0,0,0.2);"></div>
        <div class="swiper-button-next achiever-next" style="color:var(--primary); right:10px; width:50px; height:50px; background:white; border-radius:50%; box-shadow:0 4px 10px rgba(0,0,0,0.2);"></div>
        
        <div class="swiper achieversSwiper" style="width: 100%; max-width: 320px; margin: 0 auto; padding-top: 30px; padding-bottom: 60px; overflow:visible;">
          <div class="swiper-wrapper" id="achieversTrack">
            <!-- Placeholders -->
          </div>
          <div class="swiper-pagination" style="bottom:10px;"></div>
        </div>
      </div>"""

pattern = re.compile(r'<div id="achievers-slider-container-main"[^>]*>.*?</div>\s*</div>\s*</section>', re.DOTALL)
html = pattern.sub(new_html_block + '\n    </div>\n  </section>', html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update js/achievers-slider.js
js_path = r'd:\Gurudev international\Gurudev intenational\js\achievers-slider.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace Swiper config
new_swiper_config = """  if (typeof Swiper !== 'undefined') {
    new Swiper('.achieversSwiper', {
      effect: 'slide',
      grabCursor: true,
      centeredSlides: true,
      slidesPerView: 1,
      spaceBetween: 40,
      loop: displayPhotos.length >= 2,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
      navigation: {
        nextEl: '.achiever-next',
        prevEl: '.achiever-prev',
      },
      pagination: {
        el: '.swiper-pagination',
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
  }"""

js_pattern = re.compile(r'if \(typeof Swiper !== \'undefined\'\) \{.*?\}\);[\s]*\}', re.DOTALL)
js = js_pattern.sub(new_swiper_config, js)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated slider to show one by one.")
