import os

path = r'd:\Gurudev international\Gurudev intenational\erp-dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject the feature card
card_insertion_point = """      <!-- 4 -->
      <div class="feature-card border-pink">
        <div class="icon-box bg-pink-light text-pink"><i class="fa-regular fa-calendar-plus"></i></div>
        <div class="text-box">
          <h3>Apply Leave</h3>
          <p>Submit request</p>
        </div>
      </div>"""

new_card = """      <!-- 4 -->
      <div class="feature-card border-pink">
        <div class="icon-box bg-pink-light text-pink"><i class="fa-regular fa-calendar-plus"></i></div>
        <div class="text-box">
          <h3>Apply Leave</h3>
          <p>Submit request</p>
        </div>
      </div>
      <!-- 5 -->
      <div class="feature-card border-yellow" onclick="openTransportModal()" style="cursor:pointer;">
        <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>
        <div class="text-box">
          <h3>Transport Routes</h3>
          <p>Bus & Driver info</p>
        </div>
      </div>"""

if '<!-- 5 -->' not in content:
    content = content.replace(card_insertion_point, new_card)

# 2. Inject the fully styled modal at the end before </body>
styled_modal = """<!-- Transport Modal -->
<div id="transportModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(15, 23, 42, 0.7); z-index:9999; justify-content:center; align-items:center; backdrop-filter: blur(4px);">
  <div style="background:#f8fafc; width:95%; max-width:700px; border-radius:20px; overflow:hidden; box-shadow:0 25px 50px -12px rgba(0, 0, 0, 0.5); animation: fadeIn 0.3s ease; border: 1px solid rgba(255,255,255,0.2);">
    <div style="padding: 24px; background: linear-gradient(135deg, var(--primary, #0B3D91), #0a2558); color: white; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
      <h3 style="margin:0; display:flex; align-items:center; gap:10px; font-size: 1.25rem;"><i class="fa-solid fa-bus"></i> Active Transport Routes</h3>
      <button onclick="closeTransportModal()" style="background:rgba(255,255,255,0.2); border:none; color:white; width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size:1.2rem; cursor:pointer; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.3)'" onmouseout="this.style.background='rgba(255,255,255,0.2)'">&times;</button>
    </div>
    <div style="padding: 24px; max-height: 70vh; overflow-y: auto; background: #f8fafc;" id="transportModalBody">
      <div style="text-align:center; padding: 40px; color: #64748b;">
        <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2.5rem; margin-bottom: 15px; color: var(--primary, #0B3D91);"></i>
        <p style="font-weight: 500;">Loading routes from server...</p>
      </div>
    </div>
  </div>
</div>

<script type="module">
  import { db } from './js/firebase-config.js';
  import { collection, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

  window.openTransportModal = async function() {
    document.getElementById('transportModal').style.display = 'flex';
    const body = document.getElementById('transportModalBody');
    body.innerHTML = '<div style="text-align:center; padding: 40px; color: #64748b;"><i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2.5rem; margin-bottom: 15px; color: var(--primary, #0B3D91);"></i><p style="font-weight: 500;">Loading routes from server...</p></div>';
    
    try {
      const querySnapshot = await getDocs(collection(db, 'transport_routes'));
      if(querySnapshot.empty) {
        body.innerHTML = '<div style="text-align:center; padding:40px; color:#64748b;"><i class="fa-solid fa-route" style="font-size: 3rem; color:#cbd5e1; margin-bottom:15px;"></i><p style="font-size:1.1rem;">No routes available right now.</p></div>';
        return;
      }
      
      let html = '<div style="display:grid; gap:20px; padding-bottom: 10px;">';
      querySnapshot.forEach(doc => {
        const data = doc.data();
        html += `
          <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid var(--primary, #0B3D91); border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); display: flex; flex-direction: column; gap: 16px; transition: transform 0.2s ease, box-shadow 0.2s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.05)';">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; flex-wrap: wrap;">
              <div>
                <span style="background: #eef2ff; color: var(--primary, #0B3D91); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; display: inline-flex; align-items: center; gap: 6px; margin-bottom: 8px;"><i class="fa-solid fa-location-dot"></i> Route</span>
                <h4 style="margin: 0; color: #1e293b; font-size: 1.15rem; font-weight: 700;">${data.routeName || 'Unknown Route'}</h4>
              </div>
              <div style="background: var(--accent, #D4AF37); color: #fff; padding: 6px 14px; border-radius: 20px; font-size: 0.9rem; font-weight: 700; box-shadow: 0 2px 4px rgba(212, 175, 55, 0.3); display: flex; align-items: center; gap: 8px;">
                <i class="fa-solid fa-bus"></i> ${data.busNumber || 'N/A'}
              </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 16px; border-top: 1px dashed #cbd5e1; flex-wrap: wrap; gap: 12px;">
              <div style="display: flex; align-items: center; gap: 12px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: #f1f5f9; color: #64748b; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">
                  <i class="fa-solid fa-user-tie"></i>
                </div>
                <div>
                  <div style="font-size: 0.75rem; color: #64748b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Driver Details</div>
                  <div style="font-weight: 700; color: #334155; font-size: 1rem;">${data.driverName || 'Unknown'}</div>
                </div>
              </div>
              <a href="tel:${data.driverMobile}" style="background: #10b981; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; display: flex; align-items: center; gap: 10px; font-weight: 600; box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.3); transition: background 0.2s ease;" onmouseover="this.style.background='#059669'" onmouseout="this.style.background='#10b981'">
                <i class="fa-solid fa-phone-volume"></i> Call ${data.driverMobile}
              </a>
            </div>
          </div>
        `;
      });
      html += '</div>';
      body.innerHTML = html;
    } catch(err) {
      console.error(err);
      body.innerHTML = '<div style="text-align:center; padding:40px; color:#ef4444;"><i class="fa-solid fa-triangle-exclamation" style="font-size:3rem; margin-bottom:15px;"></i><p>Failed to load routes. Please check your internet connection.</p></div>';
    }
  }

  window.closeTransportModal = function() {
    document.getElementById('transportModal').style.display = 'none';
  }
</script>
</body>"""

if 'id="transportModal"' not in content:
    content = content.replace('</body>', styled_modal)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Re-added properly styled Transport feature to student dashboard.")
