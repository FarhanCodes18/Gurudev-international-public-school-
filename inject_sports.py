import re
import os

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'sports.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

interactive_html = """
  <!-- INTERACTIVE SPORTS MAP -->
  <section class="section-padding interactive-section" id="sports-map">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Campus Overview</div>
        <h2 class="section-title">Interactive <span>Sports Map</span></h2>
        <p class="section-subtitle">Click on a zone to explore the facilities.</p>
      </div>

      <div class="sports-map-container">
        <!-- SVG Map Background -->
        <div class="sports-map-visual">
          <!-- Simplified CSS layout simulating a map -->
          <div class="map-field cricket-field" data-zone="cricket">
            <span class="map-pin"><i class="fa-solid fa-location-dot"></i></span>
            <div class="map-label">Cricket Ground</div>
          </div>
          <div class="map-field football-field" data-zone="football">
            <span class="map-pin"><i class="fa-solid fa-location-dot"></i></span>
            <div class="map-label">Football Turf</div>
          </div>
          <div class="map-field basketball-court" data-zone="basketball">
            <span class="map-pin"><i class="fa-solid fa-location-dot"></i></span>
            <div class="map-label">Basketball Court</div>
          </div>
          <div class="map-field athletics-track" data-zone="athletics">
            <span class="map-pin"><i class="fa-solid fa-location-dot"></i></span>
            <div class="map-label">Athletics Track</div>
          </div>
        </div>

        <!-- Info Card Panel -->
        <div class="sports-info-panel">
          <div class="sports-info-card" id="sports-info-default">
            <i class="fa-solid fa-map-location-dot" style="font-size:3rem; color:var(--primary); margin-bottom:20px;"></i>
            <h3>Select a Zone</h3>
            <p>Click on any marker on the map to see details about the facility.</p>
          </div>
          
          <div class="sports-info-card hidden" id="sports-info-cricket">
            <div class="sports-info-image" style="background-image: url('assets/images/sports_ground.png');"></div>
            <h3>Cricket Ground</h3>
            <ul class="sports-features-list">
              <li><i class="fa-solid fa-check"></i> 65-meter boundary</li>
              <li><i class="fa-solid fa-check"></i> Turf and cemented practice nets</li>
              <li><i class="fa-solid fa-check"></i> Professional coaching available</li>
            </ul>
          </div>
          
          <div class="sports-info-card hidden" id="sports-info-football">
            <div class="sports-info-image" style="background-image: url('assets/images/sports_ground.png'); filter:hue-rotate(90deg);"></div>
            <h3>Football Turf</h3>
            <ul class="sports-features-list">
              <li><i class="fa-solid fa-check"></i> FIFA standard dimensions</li>
              <li><i class="fa-solid fa-check"></i> High-intensity floodlights</li>
              <li><i class="fa-solid fa-check"></i> Natural grass surface</li>
            </ul>
          </div>
          
          <div class="sports-info-card hidden" id="sports-info-basketball">
            <div class="sports-info-image" style="background-image: url('assets/images/sports_ground.png'); filter:saturate(2);"></div>
            <h3>Basketball Court</h3>
            <ul class="sports-features-list">
              <li><i class="fa-solid fa-check"></i> Synthetic FIBA-approved flooring</li>
              <li><i class="fa-solid fa-check"></i> Covered seating area</li>
              <li><i class="fa-solid fa-check"></i> Electronic scoreboard</li>
            </ul>
          </div>
          
          <div class="sports-info-card hidden" id="sports-info-athletics">
            <div class="sports-info-image" style="background-image: url('assets/images/sports_ground.png'); filter:grayscale(0.5);"></div>
            <h3>Athletics Track</h3>
            <ul class="sports-features-list">
              <li><i class="fa-solid fa-check"></i> 400m synthetic running track</li>
              <li><i class="fa-solid fa-check"></i> Long jump and high jump pits</li>
              <li><i class="fa-solid fa-check"></i> Shot put throwing circles</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# Insert before admission-banner
if 'id="sports-map"' not in content:
    content = content.replace(
        '<section class="admission-banner',
        interactive_html + '\n  <section class="admission-banner'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Sports Map into sports.html")
else:
    print("Sports Map already exists in sports.html")
