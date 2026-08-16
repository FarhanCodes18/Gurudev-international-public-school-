document.addEventListener('DOMContentLoaded', () => {
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
    // Append slides
    displayPhotos.forEach(photoObj => {
      track.innerHTML += createSlide(photoObj);
    });
  } else {
    // Hide slider and show the static coming soon message block
    const sliderContainer = document.getElementById('achievers-slider-container-main');
    if (sliderContainer) sliderContainer.style.display = 'none';
    const comingSoonBlock = document.getElementById('achievers-coming-soon');
    if (comingSoonBlock) comingSoonBlock.style.display = 'block';
  }

  // Initialize Swiper
    if (typeof Swiper !== 'undefined') {
    new Swiper('.achieversSwiper', {
      effect: 'slide',
      grabCursor: true,
      centeredSlides: true,
      slidesPerView: 1,
      spaceBetween: 40,
      loop: photos.length >= 2,
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
  }
});
