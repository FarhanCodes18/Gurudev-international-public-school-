import re
import os

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'science-lab.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

interactive_html = """
  <!-- INTERACTIVE VIRTUAL LAB BENCH -->
  <section class="section-padding interactive-section" id="virtual-lab">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Interactive Experience</div>
        <h2 class="section-title">Virtual <span>Lab Bench</span></h2>
        <p class="section-subtitle">Select an apparatus to see science in action.</p>
      </div>

      <div class="lab-bench-container">
        <!-- Main Display Screen -->
        <div class="lab-screen">
          <div class="lab-screen-content" id="lab-screen-default">
            <i class="fa-solid fa-microscope glow-icon"></i>
            <h3>Awaiting Experiment...</h3>
            <p>Select a module from the bench below.</p>
          </div>
          
          <div class="lab-screen-content hidden" id="lab-screen-chemistry">
            <div class="beaker">
              <div class="liquid"></div>
              <div class="bubbles"></div>
            </div>
            <h3>Chemical Reaction</h3>
            <p>Exothermic reaction generating gas bubbles.</p>
          </div>
          
          <div class="lab-screen-content hidden" id="lab-screen-physics">
            <div class="atom">
              <div class="electron orbit1"></div>
              <div class="electron orbit2"></div>
              <div class="electron orbit3"></div>
              <div class="nucleus"></div>
            </div>
            <h3>Atomic Structure</h3>
            <p>Electrons orbiting a dense nucleus.</p>
          </div>
          
          <div class="lab-screen-content hidden" id="lab-screen-biology">
            <div class="dna-strand">
               <!-- Pure CSS DNA will be drawn here -->
               <i class="fa-solid fa-dna" style="font-size:4rem; color:#10b981; animation: pulse 2s infinite;"></i>
            </div>
            <h3>DNA Sequencing</h3>
            <p>The molecular basis of inheritance.</p>
          </div>
        </div>

        <!-- The Bench (Controls) -->
        <div class="lab-bench-controls">
          <button class="lab-btn" data-target="chemistry">
            <i class="fa-solid fa-flask"></i> Chemistry
          </button>
          <button class="lab-btn" data-target="physics">
            <i class="fa-solid fa-atom"></i> Physics
          </button>
          <button class="lab-btn" data-target="biology">
            <i class="fa-solid fa-leaf"></i> Biology
          </button>
        </div>
      </div>
    </div>
  </section>
"""

# Insert before admission-banner
if 'id="virtual-lab"' not in content:
    content = content.replace(
        '<section class="admission-banner',
        interactive_html + '\n  <section class="admission-banner'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Virtual Lab into science-lab.html")
else:
    print("Virtual Lab already exists in science-lab.html")
