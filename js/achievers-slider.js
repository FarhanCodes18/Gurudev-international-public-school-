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
      
      // Clear all placeholder cards
      track.innerHTML = '';
      
      // Add only the real uploaded cards
      livePhotos.forEach(photoObj => {
        const card = document.createElement('div');
        card.className = 'achiever-card';
        card.style.cssText = 'position:absolute; width:260px; height:380px; background:var(--secondary); border-radius:16px; box-shadow:var(--shadow-xl); overflow:hidden; transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1); display:flex; flex-direction:column;';
        card.innerHTML = `
          <img src="${photoObj.image}" style="position:absolute; width:100%; height:100%; object-fit:cover; left:0; top:0; z-index:1;" alt="${photoObj.name}">
          <div class="achiever-info" style="position:absolute; bottom:0; left:0; width:100%; box-sizing:border-box; padding:80px 15px 20px; text-align:center; background:linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.6) 50%, transparent 100%); color:white; z-index:2; transition:all 0.5s ease;">
            <h3 style="font-size:1.15rem; margin-bottom:5px; font-weight:700; text-transform:uppercase; text-shadow: 0 2px 4px rgba(0,0,0,0.8); line-height:1.3;">${photoObj.name}</h3>
            <p style="font-size:0.95rem; color:#ef4444; font-weight:700; margin:0;">${photoObj.score}</p>
          </div>
        `;
        track.appendChild(card);
      });
      
      // Update our cards array so the slider logic uses the new cards
      cards = Array.from(track.querySelectorAll('.achiever-card'));
    }
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
        translateX = 180; // px
        scale = 0.85;
        opacity = 0.85;
        blur = 2;
      } else if (diff === -1) {
        translateX = -180;
        scale = 0.85;
        opacity = 0.85;
        blur = 2;
      } else if (diff >= 2) {
        translateX = 320 + ((diff - 2) * 50);
        scale = 0.7;
        opacity = 0.5;
        blur = 4;
      } else if (diff <= -2) {
        translateX = -320 - ((Math.abs(diff) - 2) * 50);
        scale = 0.7;
        opacity = 0.5;
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
      
      // Handle the text fade animation for the active card
      const infoDiv = card.querySelector('.achiever-info');
      if (infoDiv) {
        if (diff === 0) {
          infoDiv.style.opacity = '1';
          infoDiv.style.transform = 'translateY(0)';
        } else {
          infoDiv.style.opacity = '0';
          infoDiv.style.transform = 'translateY(20px)';
        }
      }
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
