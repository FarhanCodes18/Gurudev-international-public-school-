import re
import os

path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inject the UI section right before </main>
ui_block = """
        <!-- Transport Routes View -->
        <section id="view-transport" class="view-section">
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
        </section>
    </main>
"""
if 'id="view-transport"' not in content:
    content = content.replace('    </main>', ui_block)


# 2. Add addDoc, deleteDoc, doc to Firebase imports
content = re.sub(
    r"import \{ collection, query, onSnapshot \} from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';",
    "import { collection, query, onSnapshot, addDoc, deleteDoc, doc } from 'https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js';",
    content
)

# 3. Inject JS logic right before the closing tag of DOMContentLoaded:
# Find this exact block:
"""            `;
          });
        }, (error) => {
          console.error("Firebase read error:", error);
          tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:red;">Failed to connect to Firebase. Check config.</td></tr>';
        });
      }
    });"""

js_logic = """            `;
          });
        }, (error) => {
          console.error("Firebase read error:", error);
          tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:red;">Failed to connect to Firebase. Check config.</td></tr>';
        });
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

    window.deleteRoute = async function(id) {
       if(confirm("Are you sure you want to delete this route?")) {
          try {
             // Dynamically import deleteDoc and doc
             const { getFirestore, doc, deleteDoc } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
             const { app } = await import('./js/firebase-config.js');
             const db = getFirestore(app);
             await deleteDoc(doc(db, 'transport_routes', id));
          } catch(e) {
             console.error(e);
             alert("Failed to delete route.");
          }
       }
    }
"""

if 'window.deleteRoute' not in content:
    content = content.replace("""            `;
          });
        }, (error) => {
          console.error("Firebase read error:", error);
          tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; color:red;">Failed to connect to Firebase. Check config.</td></tr>';
        });
      }
    });""", js_logic)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Injected Transport UI and JS correctly!")
