/* ============================================================
   ACHIEVERS COVERFLOW SLIDER JS
   ============================================================ */
document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.achievers-slider-container');
  const track = document.getElementById('achieversTrack');
  const prevBtn = document.getElementById('achieverPrev');
  const nextBtn = document.getElementById('achieverNext');
  
  if (!track || !prevBtn || !nextBtn) return;

  let cards = Array.from(track.querySelectorAll('.achiever-card'));
  
  // --- LIVE SYNC FROM ADMIN PANEL ---
  const liveGalleryData = localStorage.getItem('admin_achievers_gallery');
  if(liveGalleryData) {
    let livePhotos = [];
    try { livePhotos = JSON.parse(liveGalleryData); } catch(e) {}
    
    if (livePhotos.length > 0) {
      const comingSoonBlock = document.getElementById('achievers-coming-soon');
      const sliderContainer = document.getElementById('achievers-slider-container-main');
      if (comingSoonBlock) comingSoonBlock.style.display = 'none';
      if (sliderContainer) sliderContainer.style.display = 'flex';
    }
    
    livePhotos.forEach((photoObj, idx) => {
      if(cards[idx]) {
        cards[idx].innerHTML = `
          <img src="${photoObj.image}" style="width:100%; height:180px; object-fit:cover;" alt="${photoObj.name}">
          <div class="achiever-info" style="padding:15px; text-align:center; background:linear-gradient(135deg, var(--bg-dark), var(--primary-dark)); color:white; flex-grow:1;">
            <h3 style="font-size:1.1rem; margin-bottom:5px;">${photoObj.name}</h3>
            <p style="font-size:0.8rem; color:var(--accent);">${photoObj.score}</p>
          </div>
        `;
      }
    });
  }

  let currentIndex = Math.floor(cards.length / 2); // Start in middle
  
  let autoSlideInterval;
  
  function updateSlider() {
    cards.forEach((card, index) => {
      card.classList.remove('active');
      const diff = index - currentIndex;
      
      // Calculate transforms
      let translateX = 0;
      let scale = 1;
      let zIndex = 10 - Math.abs(diff);
      let opacity = 1;
      let blur = 0;
      
      if (diff === 0) {
        // Active Center Card
        translateX = 0;
        scale = 1;
        card.classList.add('active');
      } else if (diff === 1) {
        translateX = 220; // px
        scale = 0.8;
        opacity = 0.8;
        blur = 2;
      } else if (diff === -1) {
        translateX = -220;
        scale = 0.8;
        opacity = 0.8;
        blur = 2;
      } else if (diff >= 2) {
        translateX = 380 + ((diff - 2) * 50);
        scale = 0.6;
        opacity = 0.4;
        blur = 4;
      } else if (diff <= -2) {
        translateX = -380 - ((Math.abs(diff) - 2) * 50);
        scale = 0.6;
        opacity = 0.4;
        blur = 4;
      }

      // Responsive mobile tweak
      if (window.innerWidth <= 768) {
        translateX = translateX * 0.7; // scale down horizontal spread
      }
      
      card.style.transform = `translateX(${translateX}px) scale(${scale})`;
      card.style.zIndex = zIndex;
      card.style.opacity = opacity;
      card.style.filter = `blur(${blur}px)`;
    });
  }

  function nextSlide() {
    if (currentIndex < cards.length - 1) {
      currentIndex++;
    } else {
      currentIndex = 0; // Loop back to start
    }
    updateSlider();
  }

  function prevSlide() {
    if (currentIndex > 0) {
      currentIndex--;
    } else {
      currentIndex = cards.length - 1; // Loop back to end
    }
    updateSlider();
  }

  function startAutoSlide() {
    stopAutoSlide();
    autoSlideInterval = setInterval(nextSlide, 3500); // Auto slide every 3.5s
  }

  function stopAutoSlide() {
    if (autoSlideInterval) {
      clearInterval(autoSlideInterval);
    }
  }

  nextBtn.addEventListener('click', () => {
    nextSlide();
    startAutoSlide(); // Reset timer on manual click
  });

  prevBtn.addEventListener('click', () => {
    prevSlide();
    startAutoSlide(); // Reset timer on manual click
  });

  // Pause auto-sliding when hovering over the slider container
  if(container) {
    container.addEventListener('mouseenter', stopAutoSlide);
    container.addEventListener('mouseleave', startAutoSlide);
  }

  // Init
  updateSlider();
  startAutoSlide();
  window.addEventListener('resize', updateSlider);
});
