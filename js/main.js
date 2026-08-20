/* ============================================================
   MAIN.JS — Core: Navbar, Scroll, Cursor, FAQ, Ripple,
              Back-to-Top, Floating Buttons, Testimonials
   ============================================================ */

(function() {
  'use strict';

  // --- CUSTOM ALERT FUNCTION ---
  function showCustomAlert(title, message, type = 'success') {
    const existingBox = document.getElementById('custom-alert-box');
    const existingOverlay = document.getElementById('custom-alert-overlay');
    if (existingBox) existingBox.remove();
    if (existingOverlay) existingOverlay.remove();

    const overlay = document.createElement('div');
    overlay.id = 'custom-alert-overlay';
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(15,23,42,0.6);backdrop-filter:blur(4px);z-index:9999;opacity:0;transition:0.3s;';

    const alertBox = document.createElement('div');
    alertBox.id = 'custom-alert-box';
    alertBox.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.9);background:#ffffff;padding:30px;border-radius:16px;box-shadow:0 20px 40px rgba(0,0,0,0.2);z-index:10000;text-align:center;min-width:300px;max-width:90%;opacity:0;transition:all 0.3s cubic-bezier(0.175,0.885,0.32,1.275);';

    const iconColor = type === 'success' ? '#10b981' : '#ef4444';
    const iconClass = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';

    alertBox.innerHTML = `
      <div style="font-size:3.5rem;color:${iconColor};margin-bottom:15px;"><i class="fa-solid ${iconClass}"></i></div>
      <h3 style="font-family:'Outfit',sans-serif;font-size:1.6rem;color:#1e293b;margin-bottom:10px;font-weight:700;">${title}</h3>
      <p style="font-family:'Poppins',sans-serif;font-size:0.95rem;color:#475569;margin-bottom:25px;line-height:1.5;">${message}</p>
      <button id="custom-alert-btn" style="background:${iconColor};color:white;border:none;padding:12px 36px;border-radius:8px;font-size:1rem;font-family:'Outfit',sans-serif;font-weight:600;cursor:pointer;transition:0.2s;box-shadow:0 4px 12px ${iconColor}40;">Okay</button>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(alertBox);

    requestAnimationFrame(() => {
      overlay.style.opacity = '1';
      alertBox.style.opacity = '1';
      alertBox.style.transform = 'translate(-50%,-50%) scale(1)';
    });

    const closeAlert = () => {
      overlay.style.opacity = '0';
      alertBox.style.opacity = '0';
      alertBox.style.transform = 'translate(-50%,-50%) scale(0.9)';
      setTimeout(() => { overlay.remove(); alertBox.remove(); }, 300);
    };

    document.getElementById('custom-alert-btn').addEventListener('click', closeAlert);
    overlay.addEventListener('click', closeAlert);
  }



  /* ===========================
     SCROLL PROGRESS BAR
  =========================== */
  const progressBar = document.getElementById('scroll-progress');
  function updateProgress() {
    if (!progressBar) return;
    const scrollTop  = window.scrollY;
    const docHeight  = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = pct + '%';
  }

  /* ===========================
     STICKY NAVBAR
  =========================== */
  const navbar = document.querySelector('.navbar');
  let lastScroll = 0;

  function handleNavbarScroll() {
    const scrollY = window.scrollY;
    if (scrollY > 80) {
      navbar && navbar.classList.add('scrolled');
    } else {
      navbar && navbar.classList.remove('scrolled');
    }
    lastScroll = scrollY;
  }

  /* ===========================
     BACK TO TOP
  =========================== */
  const backTop = document.getElementById('back-to-top');
  function handleBackTop() {
    if (!backTop) return;
    window.scrollY > 400 ? backTop.classList.add('visible') : backTop.classList.remove('visible');
  }

  backTop && backTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  /* ===========================
     COMBINED SCROLL HANDLER
  =========================== */
  window.addEventListener('scroll', function() {
    updateProgress();
    handleNavbarScroll();
    handleBackTop();
  }, { passive: true });

  // Initial call
  updateProgress();
  handleNavbarScroll();

  /* ===========================
     CUSTOM CURSOR
  =========================== */
  const cursorDot  = document.querySelector('.cursor-dot');
  const cursorRing = document.querySelector('.cursor-ring');

  let mouseX = 0, mouseY = 0;
  let ringX  = 0, ringY  = 0;

  if (cursorDot && cursorRing && window.innerWidth > 992) {
    document.body.classList.add('custom-cursor-active');

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursorDot.style.left  = mouseX + 'px';
      cursorDot.style.top   = mouseY + 'px';
    });

    // Smooth ring follow
    function animateCursor() {
      ringX += (mouseX - ringX) * 0.12;
      ringY += (mouseY - ringY) * 0.12;
      cursorRing.style.left = ringX + 'px';
      cursorRing.style.top  = ringY + 'px';
      requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Hover effect on interactive elements
    const hoverTargets = document.querySelectorAll('a, button, .btn, .gallery-item, .facility-card, .nav-link');
    hoverTargets.forEach(el => {
      el.addEventListener('mouseenter', () => cursorRing.classList.add('hovering'));
      el.addEventListener('mouseleave', () => cursorRing.classList.remove('hovering'));
    });

    // Hide cursor when out of window
    document.addEventListener('mouseleave', () => {
      cursorDot.style.opacity  = '0';
      cursorRing.style.opacity = '0';
    });
    document.addEventListener('mouseenter', () => {
      cursorDot.style.opacity  = '1';
      cursorRing.style.opacity = '1';
    });
  }

  /* ===========================
     MOUSE GLOW EFFECT
  =========================== */
  const mouseGlow = document.querySelector('.mouse-glow');
  if (mouseGlow) {
    document.addEventListener('mousemove', (e) => {
      mouseGlow.style.left = e.clientX + 'px';
      mouseGlow.style.top  = e.clientY + 'px';
    });
  }

  /* ===========================
     FAQ ACCORDION
  =========================== */
  document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', function() {
      const item = this.closest('.faq-item');
      const isOpen = item.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));

      // Toggle current
      if (!isOpen) item.classList.add('open');
    });
  });

  /* ===========================
     RIPPLE EFFECT ON BUTTONS
  =========================== */
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const rect = btn.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x    = e.clientX - rect.left - size / 2;
      const y    = e.clientY - rect.top  - size / 2;

      const ripple = document.createElement('span');
      ripple.classList.add('ripple');
      ripple.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px;`;
      btn.appendChild(ripple);

      ripple.addEventListener('animationend', () => ripple.remove());
    });
  });

  /* ===========================
     RENDER DYNAMIC REVIEWS
  =========================== */
  const reviewsTrack = document.getElementById('dynamic-reviews-track');
  if(reviewsTrack) {
    Promise.all([
      import('./js/firebase-config.js'),
      import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
    ]).then(([config, fs]) => {
       const { collection, getDocs, query, where, orderBy } = fs;
       return getDocs(query(collection(config.db, 'reviews'), where('status', '==', 'approved')));
    }).then(snapshot => {
       if(!snapshot.empty) {
         let html = '';
         snapshot.forEach(doc => {
           let r = doc.data();
           html += `
             <div class="testimonial-card">
               <div class="stars">${'★'.repeat(Number(r.rating || 5))}${'☆'.repeat(5 - Number(r.rating || 5))}</div>
               <div class="testimonial-quote">"</div>
               <p class="testimonial-text">${r.text || ''}</p>
               <div class="testimonial-author">
                 <div class="testimonial-info" style="margin-left:0;">
                   <strong>${r.name || 'Anonymous'}</strong>
                   <span>${r.role || 'Student'}</span>
                 </div>
               </div>
             </div>
           `;
         });
         reviewsTrack.innerHTML = html;
         
         // Trigger slider recalculation if necessary
         if(typeof window.initTestimonialSlider === 'function') window.initTestimonialSlider();
       } else {
         reviewsTrack.innerHTML = '<div class="testimonial-card" style="opacity:0.5;"><p class="testimonial-text">No reviews yet. Be the first to share your feedback!</p></div>';
       }
    }).catch(err => {
       console.error("Error loading reviews:", err);
    });
  }

  /* ===========================
     TESTIMONIALS SLIDER
  =========================== */
  const testSlider = document.querySelector('.testimonials-slider');
  if (testSlider) {
    const track  = testSlider.querySelector('.testimonials-track');
    const cards  = testSlider.querySelectorAll('.testimonial-card');
    const total  = cards.length;
    let current  = 0;
    let autoInterval;

    function getPerPage() {
      if (window.innerWidth < 768) return 1;
      if (window.innerWidth < 992) return 2;
      return 3;
    }

    function goToTest(index) {
      if(total === 0) return;
      const perPage = getPerPage();
      const max     = Math.max(0, total - perPage);
      current = Math.max(0, Math.min(index, max));
      const cardWidth = cards[0] ? cards[0].offsetWidth + 24 : 0; // + gap
      if(track && cardWidth > 0) track.style.transform = `translateX(${-current * cardWidth}px)`;
    }

    autoInterval = setInterval(() => {
      if(total === 0) return;
      const perPage = getPerPage();
      const max     = Math.max(0, total - perPage);
      current = current >= max ? 0 : current + 1;
      goToTest(current);
    }, 4000);

    testSlider.addEventListener('mouseenter', () => clearInterval(autoInterval));
    testSlider.addEventListener('mouseleave', () => {
      autoInterval = setInterval(() => {
        if(total === 0) return;
        const perPage = getPerPage();
        const max     = Math.max(0, total - perPage);
        current = current >= max ? 0 : current + 1;
        goToTest(current);
      }, 4000);
    });

    window.addEventListener('resize', () => goToTest(current));
  }

  // (Reviews block moved up)

  // (News rendering moved to renderNewsAndEvents() at end of file)

  /* ===========================
     SMOOTH SCROLL (Anchor Links)
  =========================== */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const navH = navbar ? navbar.offsetHeight : 0;
        const top  = target.getBoundingClientRect().top + window.scrollY - navH - 20;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

  /* ===========================
     FORM VALIDATION
  =========================== */
  document.querySelectorAll('form[data-validate]').forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      let valid = true;

      form.querySelectorAll('[required]').forEach(field => {
        const wrapper = field.closest('.form-group');
        if (!field.value.trim()) {
          valid = false;
          field.style.borderColor = 'var(--error)';
          wrapper && (wrapper.querySelector('.form-error') ||
            (() => {
              const err = document.createElement('span');
              err.className = 'form-error';
              err.style.cssText = 'color:var(--error);font-size:0.75rem;';
              err.textContent = 'This field is required.';
              wrapper.appendChild(err);
              return err;
            })());
        } else {
          field.style.borderColor = '';
          if (wrapper) {
            const err = wrapper.querySelector('.form-error');
            err && err.remove();
          }
        }
      });

      if (valid) {
        const submitBtn = form.querySelector('[type="submit"]');
        if (submitBtn) {
          submitBtn.textContent = 'Sending...';
          submitBtn.disabled    = true;
          setTimeout(() => {
            submitBtn.textContent = 'âœ“ Message Sent!';
            submitBtn.style.background = 'var(--success)';
            form.reset();
            setTimeout(() => {
              submitBtn.textContent = submitBtn.getAttribute('data-original') || 'Send Message';
              submitBtn.style.background = '';
              submitBtn.disabled = false;
            }, 3000);
          }, 1500);
        }
      }
    });

    // Live validation feedback
    form.querySelectorAll('[required]').forEach(field => {
      field.addEventListener('blur', function() {
        if (this.value.trim()) {
          this.style.borderColor = 'var(--success)';
        } else {
          this.style.borderColor = 'var(--error)';
        }
      });
    });
  });

  /* ===========================
     HERO FLOATING SHAPES
  =========================== */
  const shapesContainer = document.querySelector('.hero-shapes');
  if (shapesContainer) {
    const configs = [
      { size: 300, top: '10%',  left: '5%',   dur: 12, delay: 0 },
      { size: 200, top: '60%',  left: '80%',  dur: 10, delay: 2 },
      { size: 150, top: '80%',  left: '15%',  dur: 8,  delay: 1 },
      { size: 100, top: '30%',  left: '70%',  dur: 15, delay: 3 },
    ];

    configs.forEach(c => {
      const el = document.createElement('div');
      el.className = 'shape';
      el.style.cssText = `
        width:${c.size}px; height:${c.size}px;
        top:${c.top}; left:${c.left};
        --duration:${c.dur}s; --delay:${c.delay}s;
      `;
      shapesContainer.appendChild(el);
    });
  }

  /* ===========================
     DOWNLOAD BROCHURE
  =========================== */
  document.querySelectorAll('[data-download]').forEach(btn => {
    btn.addEventListener('click', function() {
      const href = this.getAttribute('data-download');
      if (!href) {
        // Simulate download alert
        alert('Brochure download will be available soon. Please contact us for a copy.');
        return;
      }
      const a = document.createElement('a');
      a.href = href;
      a.download = '';
      a.click();
    });
  });

  /* ===========================
     CURRENT YEAR
  =========================== */
  document.querySelectorAll('.current-year').forEach(el => {
    el.textContent = new Date().getFullYear();
  });

  // --- Faculty Slider Auto-Scroll & Animation ---
  const facultyTrack = document.getElementById('facultyTrack');
  const facultyNext = document.getElementById('facultyNext');
  const facultyPrev = document.getElementById('facultyPrev');
  let facultyAutoInterval;
  let currentFacultyIndex = 0;

  if (facultyTrack) {
    const cards = facultyTrack.querySelectorAll('.faculty-card');
    const totalCards = cards.length;

    const getVisibleCards = () => {
      if (window.innerWidth <= 576) return 1;
      if (window.innerWidth <= 768) return 2;
      if (window.innerWidth <= 991) return 3;
      return 4;
    };

    const updateSliderPosition = () => {
      const visible = getVisibleCards();
      const maxIndex = Math.max(0, totalCards - visible);
      if (currentFacultyIndex > maxIndex) currentFacultyIndex = maxIndex;
      if (currentFacultyIndex < 0) currentFacultyIndex = 0;

      const card = cards[0];
      if (card) {
        // card width + gap (30px defined in CSS)
        const style = window.getComputedStyle(facultyTrack);
        const gap = parseInt(style.gap) || 30;
        const offset = currentFacultyIndex * (card.offsetWidth + gap);
        facultyTrack.style.transform = `translateX(-${offset}px)`;
      }
    };

    const slideNextFaculty = () => {
      const visible = getVisibleCards();
      const maxIndex = Math.max(0, totalCards - visible);
      if (currentFacultyIndex >= maxIndex) {
        // loop back to start
        facultyTrack.style.opacity = '0.5';
        setTimeout(() => {
          currentFacultyIndex = 0;
          updateSliderPosition();
          facultyTrack.style.opacity = '1';
        }, 300);
      } else {
        currentFacultyIndex++;
        updateSliderPosition();
      }
    };

    const slidePrevFaculty = () => {
      if (currentFacultyIndex <= 0) {
        const visible = getVisibleCards();
        currentFacultyIndex = Math.max(0, totalCards - visible);
      } else {
        currentFacultyIndex--;
      }
      updateSliderPosition();
    };

    if (facultyNext) facultyNext.addEventListener('click', () => { slideNextFaculty(); resetFacultyAuto(); });
    if (facultyPrev) facultyPrev.addEventListener('click', () => { slidePrevFaculty(); resetFacultyAuto(); });

    const startFacultyAuto = () => {
      facultyAutoInterval = setInterval(slideNextFaculty, 3500);
    };

    const resetFacultyAuto = () => {
      clearInterval(facultyAutoInterval);
      startFacultyAuto();
    };

    startFacultyAuto();
    window.addEventListener('resize', updateSliderPosition);
    
    // Pause on hover
    facultyTrack.parentElement.addEventListener('mouseenter', () => clearInterval(facultyAutoInterval));
    facultyTrack.parentElement.addEventListener('mouseleave', startFacultyAuto);
  }

  // --- Dynamic Marquee from Admin Panel ---
  const customMarquee = localStorage.getItem('admin_marquee_text');
  if(customMarquee) {
    const marqueeTrack = document.querySelector('.marquee-track');
    if(marqueeTrack) {
      const parts = customMarquee.split('|');
      let newHtml = '';
      // We loop twice to ensure the marquee scrolling works smoothly
      for(let i = 0; i < 2; i++) {
        parts.forEach(p => {
          if(p.trim()) {
            newHtml += `<span class="marquee-item"><span class="dot"></span>${p.trim()}</span>`;
          }
        });
      }
      marqueeTrack.innerHTML = newHtml;
    }
  }


  /* ===========================
     FORM HANDLING (Admission/Contact)
  =========================== */
  const admissionForm = document.getElementById('admission-form');
  if(admissionForm) {
    admissionForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const studentName = document.getElementById('student-name') ? document.getElementById('student-name').value : '';
      const parentName = document.getElementById('parent-name') ? document.getElementById('parent-name').value : '';
      const phone = document.getElementById('adm-phone') ? document.getElementById('adm-phone').value : '';
      const applyClass = document.getElementById('apply-class') ? document.getElementById('apply-class').value : '';
      const message = document.getElementById('adm-message') ? document.getElementById('adm-message').value : '';
      
      // Combine name for generic callback format
      const finalName = studentName ? `${studentName} (Child of ${parentName})` : parentName;
      const actionUrl = admissionForm.getAttribute('action');
      const submitBtn = admissionForm.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : '';
      if(submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

      Promise.all([
        import('./js/firebase-config.js'),
        import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
      ]).then(([config, fs]) => {
         return fs.addDoc(fs.collection(config.db, 'callbacks'), {
           date: new Date().toLocaleDateString('en-GB'),
           name: finalName,
           phone: phone,
           class: applyClass || 'General Inquiry',
           message: message,
           timestamp: Date.now()
         });
      }).then(() => {
        if (actionUrl && actionUrl !== '#') {
          const formData = new FormData(admissionForm);
          return fetch(actionUrl, { method: 'POST', body: formData, headers: { 'Accept': 'application/json' } });
        }
      }).then(() => {
        alert("Application Submitted Successfully! Our admission team will contact you shortly.");
        admissionForm.reset();
        if(submitBtn) submitBtn.innerHTML = originalText;
      }).catch(error => {
        console.error("Firebase/Fetch Error:", error);
        alert("Error submitting application. Please try again.");
        if(submitBtn) submitBtn.innerHTML = originalText;
      });
    });
  }

  // Handle Contact Form Submission
  const contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const name = document.getElementById('name') ? document.getElementById('name').value : '';
      const phone = document.getElementById('phone') ? document.getElementById('phone').value : '';
      const email = document.getElementById('email') ? document.getElementById('email').value : '';
      const subject = document.getElementById('subject') ? document.getElementById('subject').value : '';
      const message = document.getElementById('message') ? document.getElementById('message').value : '';
      const actionUrl = contactForm.getAttribute('action');
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : '';
      if(submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

      Promise.all([
        import('./js/firebase-config.js'),
        import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
      ]).then(([config, fs]) => {
         return fs.addDoc(fs.collection(config.db, 'contact_messages'), {
           date: new Date().toLocaleDateString('en-GB'),
           name: name,
           phone: phone,
           email: email,
           subject: subject,
           message: message,
           timestamp: Date.now()
         });
      }).then(() => {
        if (actionUrl && actionUrl !== '#') {
          const formData = new FormData(contactForm);
          return fetch(actionUrl, { method: 'POST', body: formData, headers: { 'Accept': 'application/json' } });
        }
      }).then(() => {
        alert("Thank you! Your message has been sent. We will get back to you shortly.");
        contactForm.reset();
        if(submitBtn) submitBtn.innerHTML = originalText;
      }).catch(error => {
        console.error("Firebase/Fetch Error:", error);
        alert("Error sending message. Please try again.");
        if(submitBtn) submitBtn.innerHTML = originalText;
      });
    });
  }

  // Handle Feedback Form Submission
  const feedbackForm = document.getElementById('feedback-form');
  if(feedbackForm) {
    feedbackForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const name = document.getElementById('fb-name').value;
      const role = document.getElementById('fb-role').value;
      const rating = document.getElementById('fb-rating').value;
      const message = document.getElementById('fb-message').value;
      const submitBtn = feedbackForm.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : '';
      if(submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

      Promise.all([
        import('./js/firebase-config.js'),
        import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
      ]).then(([config, fs]) => {
         return fs.addDoc(fs.collection(config.db, 'reviews'), {
           name: name,
           role: role,
           rating: rating,
           text: message,
           status: 'pending',
           date: new Date().toLocaleDateString('en-GB'),
           timestamp: Date.now()
         });
      }).then(() => {
        const modalContent = document.querySelector('#feedback-modal .modal-content');
        if (modalContent) {
          modalContent.innerHTML = `
            <div style="text-align:center; padding: 40px 20px;">
              <i class="fa-solid fa-circle-check" style="font-size: 4rem; color: #16a34a; margin-bottom: 20px;"></i>
              <h3 style="margin-bottom: 15px; color: var(--heading-color);">Thank You!</h3>
              <p style="color: var(--text-color); margin-bottom: 30px;">Your feedback has been successfully submitted and is pending admin approval.</p>
              <button class="btn btn-primary" onclick="document.getElementById('feedback-modal').classList.remove('active'); setTimeout(() => window.location.reload(), 300);">Close</button>
            </div>
          `;
        } else {
          alert("Thank you for your feedback! It has been submitted to the admin for approval.");
          feedbackForm.reset();
          document.getElementById('feedback-modal').classList.remove('active');
        }
      }).catch(error => {
         console.error("Firebase Error:", error);
         alert("Error submitting feedback. Please try again.");
         if(submitBtn) submitBtn.innerHTML = originalText;
      });
    });
  }

  // ============================================================
  // GLOBAL QUICK CALLBACK POPUP
  // ============================================================
  if (!sessionStorage.getItem('quickCallbackShown')) {
  setTimeout(() => {
    // Inject Modal HTML
    const modalHTML = `
      <div id="quick-callback-modal">
        <div class="qc-modal-content" style="border-radius:24px; overflow:hidden;">
          <button class="qc-close" id="qc-close-btn" style="background:#fff; color:#333; box-shadow:0 4px 10px rgba(0,0,0,0.1);"><i class="fa-solid fa-xmark"></i></button>
          
          <div class="qc-left" style="background: linear-gradient(135deg, #1d4ed8, #1e3a8a); position:relative; overflow:hidden;">
            <div style="position:absolute; top:-50px; left:-50px; width:150px; height:150px; background:rgba(255,255,255,0.1); border-radius:50%;"></div>
            <div style="position:absolute; bottom:-30px; right:-30px; width:100px; height:100px; background:rgba(255,255,255,0.1); border-radius:50%;"></div>
            <div class="qc-left-content" style="position:relative; z-index:2;">
              <div style="font-size:2rem; margin-bottom:15px; color:#facc15;"><i class="fa-solid fa-graduation-cap"></i></div>
              <h3>Admissions Open 2026-27</h3>
              <p>Secure your child's future at Gurudev International Public School.</p>
              <ul style="margin-top:20px;">
                <li style="margin-bottom:10px;"><i class="fa-solid fa-check-circle" style="color:#facc15;"></i> Experienced Faculty</li>
                <li style="margin-bottom:10px;"><i class="fa-solid fa-check-circle" style="color:#facc15;"></i> Modern Infrastructure</li>
                <li><i class="fa-solid fa-check-circle" style="color:#facc15;"></i> Holistic Development</li>
              </ul>
            </div>
          </div>
          
          <div class="qc-right">
            <div class="qc-header">
              <h4 style="color:#2563eb; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Admissions Helpdesk</h4>
              <h2 style="font-weight:800; color:#0f172a;">Let's Connect!</h2>
              <p>Fill out the details below and our team will guide you through the process.</p>
            </div>
            <form id="quick-callback-form" class="qc-form" action="https://formspree.io/f/mppardbk" method="POST">
              <div class="qc-form-row" style="display:none;">
                <input type="hidden" id="qc-program" name="program" value="N/A" />
                <input type="hidden" id="qc-branch" name="branch" value="N/A" />
              </div>
              <div class="qc-form-row">
                <input type="text" id="qc-name" name="name" class="qc-input" placeholder="Full Name *" required />
                <input type="tel" id="qc-phone" name="phone" class="qc-input" placeholder="Phone Number *" required />
              </div>
              <input type="email" id="qc-email" name="email" class="qc-input" placeholder="Email Address *" required />
              <input type="text" id="qc-address" name="address" class="qc-input" placeholder="Address *" required />
              <input type="text" id="qc-message" name="message" class="qc-input" placeholder="Message (optional)" />
              <button type="submit" class="qc-submit">Request Callback</button>
            </form>
          </div>
        </div>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    const modal = document.getElementById('quick-callback-modal');
    const closeBtn = document.getElementById('qc-close-btn');
    const form = document.getElementById('quick-callback-form');
    
    // Show Modal
    setTimeout(() => {
      modal.classList.add('active');
    }, 50);
    
    // Close Logic
    closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.classList.remove('active');
    });
    
    // Form Submission
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const lead = {
        date: new Date().toLocaleDateString('en-GB'),
        program: document.getElementById('qc-program').value,
        branch: document.getElementById('qc-branch').value,
        name: document.getElementById('qc-name').value,
        phone: document.getElementById('qc-phone').value,
        email: document.getElementById('qc-email').value,
        address: document.getElementById('qc-address').value,
        message: document.getElementById('qc-message').value
      };
      const actionUrl = form.getAttribute('action');
      const submitBtn = form.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : '';
      if(submitBtn) submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

      Promise.all([
        import('./js/firebase-config.js'),
        import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
      ]).then(([config, fs]) => {
         return fs.addDoc(fs.collection(config.db, 'quick_callbacks'), {
           ...lead,
           timestamp: Date.now()
         });
      }).then(() => {
        if (actionUrl && actionUrl !== '#') {
          const formData = new FormData(form);
          return fetch(actionUrl, { method: 'POST', body: formData, headers: { 'Accept': 'application/json' } });
        }
      }).then(() => {
        alert("Thank you! Our admission counselor will call you shortly.");
        form.reset();
        if(submitBtn) submitBtn.innerHTML = originalText;
        modal.classList.remove('active');
      }).catch(error => {
        console.error("Firebase/Fetch Error:", error);
        alert("Error sending request. Please try again.");
        if(submitBtn) submitBtn.innerHTML = originalText;
      });
    });
    
  sessionStorage.setItem('quickCallbackShown', 'true');
    }, 2000); // 2-second delay
  }

  /* ===========================
     MOBILE FOOTER ACCORDION
  =========================== */
  const footerTitles = document.querySelectorAll('.footer-col-title');
  footerTitles.forEach(title => {
    title.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        const parentCol = title.closest('.footer-col');
        parentCol.classList.toggle('open');
      }
    });
  });

  /* ===========================
     COMPLAINT / GENERAL FORM HANDLER
  =========================== */
  const complaintForm = document.getElementById('complaint-form');
  if(complaintForm) {
    complaintForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const submitBtn = complaintForm.querySelector('button[type="submit"]');
      const originalText = submitBtn ? submitBtn.innerHTML : 'Submit';
      if(submitBtn) {
         submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Submitting...';
         submitBtn.disabled = true;
      }
      
      const fd = new FormData(complaintForm);
      const data = Object.fromEntries(fd.entries());
      
      Promise.all([
        import('./js/firebase-config.js'),
        import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js')
      ]).then(([config, fs]) => {
         return fs.addDoc(fs.collection(config.db, 'complaints'), {
            ...data,
            date: new Date().toLocaleDateString('en-GB'),
            timestamp: Date.now()
         });
      }).then(() => {
         alert("Thank you! Your complaint/message has been submitted successfully.");
         complaintForm.reset();
      }).catch(error => {
         console.error("Firebase Error:", error);
         alert("Error submitting form. Please try again.");
      }).finally(() => {
         if(submitBtn) {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
         }
      });
    });
  }

  /* ===========================
     DYNAMIC NEWS & EVENTS
  =========================== */
  function renderNewsAndEvents() {
    const grids = [
      document.getElementById('dynamic-news-grid'),
      document.getElementById('news-page-grid')
    ];
    
    let newsList = JSON.parse(localStorage.getItem('admin_news_events')) || [];
    
    grids.forEach(grid => {
      if(!grid) return;
      grid.innerHTML = '';
      
      if(newsList.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; color: var(--text-color); padding: 40px;">No news or events published yet. Check back later!</div>';
        return;
      }
      
      newsList.forEach((news, idx) => {
        // Limit to 3 on homepage, show all on news page
        if(grid.id === 'dynamic-news-grid' && idx >= 3) return;
        
        const photo = news.image || 'assets/images/hero-3.jpg';
        grid.innerHTML += `
          <article class='news-card' data-aos='fade-up' data-aos-delay='${(idx % 3 + 1) * 100}'>
            <div class='news-image'>
              <img src='${photo}' alt='${news.title}' loading='lazy' style='object-fit:cover; width:100%; height:100%;' />
              <span class='news-category'>${news.category}</span>
            </div>
            <div class='news-body'>
              <div class='news-meta'>
                <span class='news-meta-item'><i class='fa-regular fa-calendar'></i> ${news.date}</span>
              </div>
              <h3 class='news-title'>${news.title}</h3>
              <p class='news-excerpt'>${news.excerpt}</p>
              <a href='news.html' class='news-read-more'>Read More <i class='fa-solid fa-arrow-right'></i></a>
            </div>
          </article>
        `;
      });
    });
  }
  renderNewsAndEvents();

})();



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
document.addEventListener("contextmenu", (e) => e.preventDefault());
document.addEventListener("keydown", (e) => {
  if (e.key === "F12" || (e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "J" || e.key === "C")) || (e.ctrlKey && e.key === "U")) {
    e.preventDefault();
  }
});

