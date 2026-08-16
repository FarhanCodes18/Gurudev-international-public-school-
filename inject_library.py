import re
import os

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'library.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

interactive_html = """
  <!-- INTERACTIVE 3D BOOKSHELF -->
  <section class="section-padding interactive-section" id="virtual-library" style="background:var(--bg-section);">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Digital Catalog</div>
        <h2 class="section-title">Explore Our <span>Collection</span></h2>
        <p class="section-subtitle">Hover and click to explore featured books.</p>
      </div>

      <div class="bookshelf-container">
        <div class="bookshelf">
          <!-- Book 1 -->
          <div class="book-container">
            <div class="book">
              <div class="book-front" style="background: linear-gradient(135deg, #1e3a8a, #3b82f6);">
                <div class="book-title">A Brief History<br>of Time</div>
                <div class="book-author">Stephen Hawking</div>
              </div>
              <div class="book-spine"></div>
              <div class="book-back">
                <p>A landmark volume in science writing by one of the great minds of our time.</p>
                <button class="book-btn">Read Now</button>
              </div>
            </div>
          </div>
          <!-- Book 2 -->
          <div class="book-container">
            <div class="book">
              <div class="book-front" style="background: linear-gradient(135deg, #7c2d12, #ef4444);">
                <div class="book-title">Hamlet</div>
                <div class="book-author">William Shakespeare</div>
              </div>
              <div class="book-spine"></div>
              <div class="book-back">
                <p>The tragedy of the Prince of Denmark. A masterpiece of English literature.</p>
                <button class="book-btn">Read Now</button>
              </div>
            </div>
          </div>
          <!-- Book 3 -->
          <div class="book-container">
            <div class="book">
              <div class="book-front" style="background: linear-gradient(135deg, #064e3b, #10b981);">
                <div class="book-title">Origin of<br>Species</div>
                <div class="book-author">Charles Darwin</div>
              </div>
              <div class="book-spine"></div>
              <div class="book-back">
                <p>The foundation of evolutionary biology. Groundbreaking natural history.</p>
                <button class="book-btn">Read Now</button>
              </div>
            </div>
          </div>
          <!-- Book 4 -->
          <div class="book-container">
            <div class="book">
              <div class="book-front" style="background: linear-gradient(135deg, #4c1d95, #8b5cf6);">
                <div class="book-title">Calculus<br>Vol. 1</div>
                <div class="book-author">Tom M. Apostol</div>
              </div>
              <div class="book-spine"></div>
              <div class="book-back">
                <p>A comprehensive introduction to mathematics for students of science and engineering.</p>
                <button class="book-btn">Read Now</button>
              </div>
            </div>
          </div>
        </div>
        <div class="shelf-board"></div>
      </div>
    </div>
  </section>
"""

# Insert before admission-banner
if 'id="virtual-library"' not in content:
    content = content.replace(
        '<section class="admission-banner',
        interactive_html + '\n  <section class="admission-banner'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Library Bookshelf into library.html")
else:
    print("Library Bookshelf already exists in library.html")
