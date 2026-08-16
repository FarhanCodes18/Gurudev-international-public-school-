import re

path = r'd:\Gurudev international\Gurudev intenational\erp-dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the card to be clickable
old_card = """        <div class="feature-card border-yellow">
          <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>
          <div class="text-box">
            <h3>Transport Routes</h3>
            <p>Bus & Driver info</p>
          </div>
        </div>"""

new_card = """        <div class="feature-card border-yellow" onclick="openTransportModal()" style="cursor:pointer;">
          <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>
          <div class="text-box">
            <h3>Transport Routes</h3>
            <p>Bus & Driver info</p>
          </div>
        </div>"""

if 'onclick="openTransportModal()"' not in content:
    content = content.replace(old_card, new_card)

# 2. Add Modal UI before closing </body>
modal_ui = """
<!-- Transport Modal -->
<div id="transportModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:9999; justify-content:center; align-items:center;">
  <div style="background:var(--white); width:90%; max-width:600px; border-radius:var(--radius-xl); overflow:hidden; box-shadow:var(--shadow-xl); animation: fadeIn 0.3s ease;">
    <div style="padding: 20px; background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: var(--white); display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin:0; display:flex; align-items:center; gap:10px;"><i class="fa-solid fa-bus"></i> Active Transport Routes</h3>
      <button onclick="closeTransportModal()" style="background:none; border:none; color:white; font-size:1.5rem; cursor:pointer;">&times;</button>
    </div>
    <div style="padding: 20px; max-height: 70vh; overflow-y: auto;" id="transportModalBody">
      <div style="text-align:center; padding: 40px; color: var(--text-muted);">
        <i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2rem; margin-bottom: 10px;"></i>
        <p>Loading routes...</p>
      </div>
    </div>
  </div>
</div>
"""
if 'id="transportModal"' not in content:
    content = content.replace('</body>', modal_ui + '\n</body>')


# 3. Add JS logic
js_logic = """
<script type="module">
  import { db } from './js/firebase-config.js';
  import { collection, getDocs } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';

  window.openTransportModal = async function() {
    document.getElementById('transportModal').style.display = 'flex';
    const body = document.getElementById('transportModalBody');
    body.innerHTML = '<div style="text-align:center; padding: 40px; color: var(--text-muted);"><i class="fa-solid fa-circle-notch fa-spin" style="font-size: 2rem; margin-bottom: 10px;"></i><p>Loading routes...</p></div>';
    
    try {
      const querySnapshot = await getDocs(collection(db, 'transport_routes'));
      if(querySnapshot.empty) {
        body.innerHTML = '<div style="text-align:center; padding:40px; color:var(--text-muted);">No routes available right now.</div>';
        return;
      }
      
      let html = '<div style="display:grid; gap:16px;">';
      querySnapshot.forEach(doc => {
        const data = doc.data();
        html += `
          <div style="border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 16px; display:flex; flex-direction:column; gap:12px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <h4 style="margin:0; color:var(--primary); display:flex; align-items:center; gap:8px;"><i class="fa-solid fa-route"></i> ${data.routeName || 'Unknown Route'}</h4>
              <span style="background:var(--secondary); padding:4px 12px; border-radius:20px; font-size:0.85rem; font-weight:600;"><i class="fa-solid fa-bus"></i> ${data.busNumber || 'N/A'}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; padding-top:12px; border-top:1px dashed var(--border-color);">
              <div>
                <div style="font-size:0.85rem; color:var(--text-muted);">Driver Name</div>
                <div style="font-weight:600;">${data.driverName || 'Unknown'}</div>
              </div>
              <a href="tel:${data.driverMobile}" style="background: var(--success); color: white; padding: 8px 16px; border-radius: var(--radius-sm); text-decoration: none; display:flex; align-items:center; gap:8px; font-weight:500;">
                <i class="fa-solid fa-phone"></i> Call Driver
              </a>
            </div>
          </div>
        `;
      });
      html += '</div>';
      body.innerHTML = html;
    } catch(err) {
      console.error(err);
      body.innerHTML = '<div style="text-align:center; padding:40px; color:var(--danger);">Failed to load routes. Please try again.</div>';
    }
  }

  window.closeTransportModal = function() {
    document.getElementById('transportModal').style.display = 'none';
  }
</script>
"""

if 'window.openTransportModal' not in content:
    content = content.replace('</body>', js_logic + '\n</body>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated erp-dashboard.html successfully.")
