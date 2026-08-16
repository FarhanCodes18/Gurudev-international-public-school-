import re

path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add sidebar link
old_sidebar = """          <a class="nav-item" data-view="certificate"><i class="fa-solid fa-award"></i> Certificate Maker</a>
        </div>"""
new_sidebar = """          <a class="nav-item" data-view="certificate"><i class="fa-solid fa-award"></i> Certificate Maker</a>
          <a class="nav-item" data-view="transport"><i class="fa-solid fa-bus"></i> Transport Routes</a>
        </div>"""
if 'data-view="transport"' not in content:
    content = content.replace(old_sidebar, new_sidebar)


# 2. Add view section
old_view = """      </main>
    </div>"""

transport_view = """        <!-- Transport Routes View -->
        <div class="admin-view" id="view-transport" style="display:none;">
          <div class="admin-card">
            <h3>Add New Transport Route</h3>
            <form id="addRouteForm" style="display: grid; gap: 16px; margin-top: 20px;">
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <input type="text" id="routeName" class="form-control" placeholder="Route Name / Area (e.g., Route 1 - City Center)" required>
                <input type="text" id="busNumber" class="form-control" placeholder="Bus Number (e.g., MP-50-P-1234)" required>
              </div>
              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <input type="text" id="driverName" class="form-control" placeholder="Driver Name" required>
                <input type="text" id="driverMobile" class="form-control" placeholder="Driver Mobile Number" required>
              </div>
              <button type="submit" class="btn btn-primary" style="width: 200px;">Add Route</button>
            </form>
          </div>

          <div class="admin-card" style="margin-top: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
              <h3>Active Transport Routes</h3>
            </div>
            <div style="overflow-x: auto;">
              <table class="admin-table">
                <thead>
                  <tr>
                    <th>Route / Area</th>
                    <th>Bus Number</th>
                    <th>Driver Name</th>
                    <th>Driver Mobile</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody id="superadmin-routes-list">
                  <tr><td colspan="5" style="text-align:center;">Loading routes...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </main>
    </div>"""
if 'id="view-transport"' not in content:
    content = content.replace(old_view, transport_view)

# 3. Add Firebase imports & logic
old_fb_import = "import { collection, query, onSnapshot } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';"
new_fb_import = "import { collection, query, onSnapshot, addDoc, deleteDoc, doc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';"
if 'addDoc' not in content:
    content = content.replace(old_fb_import, new_fb_import)

old_fb_script_end = """          });
        }
      });
    </script>"""

new_fb_script_end = """          });
        }

        // --- Transport Routes Logic ---
        const routeForm = document.getElementById('addRouteForm');
        if(routeForm && db) {
           routeForm.addEventListener('submit', async (e) => {
              e.preventDefault();
              const routeName = document.getElementById('routeName').value.trim();
              const busNumber = document.getElementById('busNumber').value.trim();
              const driverName = document.getElementById('driverName').value.trim();
              const driverMobile = document.getElementById('driverMobile').value.trim();
              
              try {
                 await addDoc(collection(db, 'transport_routes'), {
                    routeName, busNumber, driverName, driverMobile, createdAt: new Date().toISOString()
                 });
                 routeForm.reset();
                 alert("Route Added Successfully!");
              } catch(err) {
                 console.error(err);
                 alert("Error adding route.");
              }
           });

           // Fetch Routes
           const routeBody = document.getElementById('superadmin-routes-list');
           onSnapshot(query(collection(db, 'transport_routes')), (snapshot) => {
              if (snapshot.empty) {
                 routeBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No routes active yet.</td></tr>';
                 return;
              }
              routeBody.innerHTML = '';
              snapshot.forEach((d) => {
                 const data = d.data();
                 routeBody.innerHTML += `
                   <tr>
                     <td style="font-weight:600; color:var(--primary);">${data.routeName || 'N/A'}</td>
                     <td>${data.busNumber || 'N/A'}</td>
                     <td>${data.driverName || 'N/A'}</td>
                     <td>${data.driverMobile || 'N/A'}</td>
                     <td>
                        <button class="btn-admin-outline" onclick="deleteRoute('${d.id}')" style="color:var(--admin-danger); border-color:var(--admin-danger); padding: 4px 8px;">Delete</button>
                     </td>
                   </tr>
                 `;
              });
           });
        }
      });

      // Global delete function for Routes
      window.deleteRoute = async function(id) {
         if(confirm("Are you sure you want to delete this route?")) {
            const { db } = await import('./js/firebase-config.js');
            const { doc, deleteDoc } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
            try {
               await deleteDoc(doc(db, 'transport_routes', id));
            } catch(e) {
               alert("Failed to delete route.");
            }
         }
      }
    </script>"""

if 'window.deleteRoute' not in content:
    content = content.replace(old_fb_script_end, new_fb_script_end)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated gurudev-super.html successfully.")
