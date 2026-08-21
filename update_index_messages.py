import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = '''        <div class="messages-grid">

        <!-- Vice President -->
        <div class="message-card" data-aos="fade-up" data-aos-delay="100">
          <div class="message-card-top">
            <img src="assets/images/ravi meghe.png" alt="Vice President" class="message-avatar" style="width:auto;height:120px;border-radius:12px;object-fit:cover;" loading="lazy" />
            <div class="message-name">Mr. Ravi Meghe</div>
            <div class="message-title">Vice President</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 5px; font-weight: 500;">Gurudev Shikshan Samiti</div>
          </div>
          <div class="message-card-body">
            <p class="message-text">
              "We are committed to providing an environment where every student is empowered to discover their true potential. Our focus remains on holistic development and academic excellence."
            </p>
            <a href="management-committee.html" class="message-read-more">
              Read Full Message <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </div>

        <!-- Treasurer -->
        <div class="message-card" data-aos="fade-up" data-aos-delay="200">
          <div class="message-card-top">
            <img src="assets/images/chandrakant tiwari.png" alt="Treasurer" class="message-avatar" style="width:auto;height:120px;border-radius:12px;object-fit:cover;" loading="lazy" />
            <div class="message-name">Mr. Chandrakant Tiwari</div>
            <div class="message-title">Treasurer</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 5px; font-weight: 500;">Gurudev Shikshan Samiti</div>
          </div>
          <div class="message-card-body">
            <p class="message-text">
              "Our goal is to ensure that the resources of this institution are utilized effectively to provide world-class facilities, fostering an atmosphere conducive to modern learning."
            </p>
            <a href="management-committee.html" class="message-read-more">
              Read Full Message <i class="fa-solid fa-arrow-right"></i>
            </a>
          </div>
        </div>'''

pattern = r'<div class="messages-grid">\s*<!-- Secretary -->.*?<!-- Principal -->'
html = re.sub(pattern, replacement + '\n\n        <!-- Principal -->', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html successfully.")
