import os
import re

path = r'd:\Gurudev international\Gurudev intenational\erp-dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the openTransportModal JS logic to ONLY show ONE card (the most recent one or the first one it finds)
# We will just break out of the forEach loop after the first iteration, or we can just get the first doc from docs array.

old_js = """      let html = '<div style="display:grid; gap:20px; padding-bottom: 10px;">';
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
      html += '</div>';"""

new_js = """      // Automatically just show the very LAST added route to prevent duplicates showing up
      const doc = querySnapshot.docs[querySnapshot.docs.length - 1]; // get the last added one
      const data = doc.data();
      
      let html = '<div style="display:grid; gap:20px; padding-bottom: 10px;">';
      html += `
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-left: 5px solid var(--primary, #0B3D91); border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); display: flex; flex-direction: column; gap: 16px; transition: transform 0.2s ease, box-shadow 0.2s ease;" onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 15px -3px rgba(0, 0, 0, 0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 6px -1px rgba(0, 0, 0, 0.05)';">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; flex-wrap: wrap;">
            <div>
              <span style="background: #eef2ff; color: var(--primary, #0B3D91); padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; display: inline-flex; align-items: center; gap: 6px; margin-bottom: 8px;"><i class="fa-solid fa-location-dot"></i> Assigned Route</span>
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
      html += '</div>';"""

if 'querySnapshot.forEach(doc => {' in content:
    content = content.replace(old_js, new_js)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed modal to ONLY show one route.")
else:
    print("Could not find the JS block to replace.")
