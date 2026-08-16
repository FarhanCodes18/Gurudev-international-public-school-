import os
import re

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'index.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject Swiper CSS
if 'swiper-bundle.min.css' not in content:
    content = content.replace(
        '<link rel="stylesheet" href="css/style.css" />',
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.css" />\n  <link rel="stylesheet" href="css/style.css" />'
    )

# 2. Inject Swiper JS
if 'swiper-bundle.min.js' not in content:
    content = content.replace(
        '<script src="js/main.js"></script>',
        '<script src="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>\n  <script src="js/main.js"></script>'
    )

# 3. Construct 35 Teacher Cards HTML
cards_html = ""
for i in range(1, 36):
    cards_html += f"""
          <!-- Slide {i} -->
          <div class="swiper-slide">
            <div class="cse-faculty-card">
              <div class="cse-faculty-img">
                <img src="assets/images/teacher-1.jpg" alt="CSE Teacher {i}" loading="lazy" onerror="this.src='assets/icons/gurudev_school-removebg-preview.png'">
                <div class="cse-faculty-overlay">
                  <a href="#"><i class="fa-brands fa-linkedin-in"></i></a>
                  <a href="#"><i class="fa-solid fa-envelope"></i></a>
                </div>
              </div>
              <div class="cse-faculty-info">
                <h3>Professor Name {i}</h3>
                <p class="designation">CSE Department</p>
                <p class="specialization">M.Tech, AI & Data Science</p>
              </div>
            </div>
          </div>
"""

# 4. Construct Section HTML
section_html = f"""
  <!-- CSE FACULTY SWIPER SECTION -->
  <section class="cse-section section-padding" id="cse-faculty" style="background:var(--bg-section); overflow:hidden;">
    <div class="container">
      <div class="section-header" style="text-align: center;">
        <div class="section-label" data-aos="fade-up">OUR FACULTY</div>
        <h2 class="section-title" data-aos="fade-up" data-aos-delay="100">The Minds That <span>Code The Future</span></h2>
        <p class="section-subtitle" data-aos="fade-up" data-aos-delay="200" style="max-width:800px; margin: 20px auto 40px; line-height: 1.8;">Our CSE faculty blend academic excellence with real-world innovation, mentoring students to become problem solvers, innovators, and future tech leaders.</p>
      </div>
      
      <!-- Swiper Container -->
      <div class="swiper cseSwiper" data-aos="fade-up" data-aos-delay="300">
        <div class="swiper-wrapper">
{cards_html}
        </div>
        
        <!-- Navigation & Pagination -->
        <div class="swiper-pagination"></div>
        <div class="swiper-button-next cse-next"></div>
        <div class="swiper-button-prev cse-prev"></div>
      </div>
    </div>
  </section>
"""

# 5. Inject HTML into index.html
if 'id="cse-faculty"' not in content:
    content = content.replace(
        '<section class="testimonials-section',
        section_html + '\n  <section class="testimonials-section'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected CSE Faculty section into index.html")
else:
    print("CSE Faculty section already exists.")

# 6. Append CSS and JS logic directly into interactive.css and interactive.js (or just output it for another script)
