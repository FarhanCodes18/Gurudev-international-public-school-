import os

path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will replace the ugly transport view with a beautifully styled one using the admin panel's native classes.
old_view = """        <section id="view-transport" class="view-section">
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
        </section>"""

new_view = """        <section id="view-transport" class="view-section">
          <div class="page-header">
            <div>
              <h2 class="page-title"><i class="fa-solid fa-bus"></i> Transport Management</h2>
              <p class="page-desc">Manage school bus routes, driver details, and contact numbers. These will instantly sync to the student portals.</p>
            </div>
          </div>
          
          <div class="form-card" style="margin-bottom: 30px;">
            <div class="table-title" style="margin-bottom: 20px; font-size: 1.2rem;">Add New Transport Route</div>
            <form id="addRouteForm" style="display: grid; gap: 20px;">
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div class="admin-form-group" style="margin: 0;">
                  <label for="routeName">Route Name / Area</label>
                  <input type="text" id="routeName" class="admin-input" placeholder="e.g., Route 1 - City Center" required>
                </div>
                <div class="admin-form-group" style="margin: 0;">
                  <label for="busNumber">Bus Number</label>
                  <input type="text" id="busNumber" class="admin-input" placeholder="e.g., MP-50-P-1234" required>
                </div>
              </div>
              
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div class="admin-form-group" style="margin: 0;">
                  <label for="driverName">Driver Name</label>
                  <input type="text" id="driverName" class="admin-input" placeholder="Enter driver's full name" required>
                </div>
                <div class="admin-form-group" style="margin: 0;">
                  <label for="driverMobile">Driver Mobile Number</label>
                  <input type="tel" id="driverMobile" class="admin-input" placeholder="e.g., 9876543210" required>
                </div>
              </div>
              
              <button type="submit" class="btn-admin" style="justify-self: start; min-width: 200px; justify-content: center; margin-top: 10px;">
                <i class="fa-solid fa-plus"></i> Add New Route
              </button>
            </form>
          </div>

          <div class="table-container">
            <div class="table-header">
              <div class="table-title">Active Transport Routes</div>
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
        </section>"""

if 'id="routeName" class="form-control"' in content:
    content = content.replace(old_view, new_view)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated transport view with beautiful CSS styling.")
