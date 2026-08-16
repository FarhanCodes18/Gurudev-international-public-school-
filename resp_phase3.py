
# Add mobile sidebar toggle JS to gurudev-super.html and erp-admin.html
import os

base = r'd:\Gurudev international\Gurudev intenational'

sidebar_js = """
<script>
/* Mobile sidebar toggle for admin/super admin */
(function() {
  var sidebar = document.querySelector('.admin-sidebar');
  var overlay = document.querySelector('.admin-mobile-overlay');
  var toggle  = document.querySelector('.admin-mobile-toggle');

  if (!sidebar) return;

  // Create overlay if missing
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.className = 'admin-mobile-overlay';
    document.body.appendChild(overlay);
  }

  // Create toggle button if missing in topbar
  if (!toggle) {
    var topbar = document.querySelector('.admin-topbar');
    if (topbar) {
      toggle = document.createElement('button');
      toggle.className = 'admin-mobile-toggle';
      toggle.innerHTML = '<i class="fa-solid fa-bars"></i>';
      topbar.insertBefore(toggle, topbar.firstChild);
    }
  }

  function openSidebar() {
    sidebar.classList.add('open');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
  function closeSidebar() {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (toggle) toggle.addEventListener('click', openSidebar);
  overlay.addEventListener('click', closeSidebar);

  // Close on nav item click (mobile)
  var navItems = sidebar.querySelectorAll('.nav-item, a');
  navItems.forEach(function(el) {
    el.addEventListener('click', function() {
      if (window.innerWidth <= 992) closeSidebar();
    });
  });
})();
</script>
"""

targets = ['gurudev-super.html', 'erp-admin.html']

for fname in targets:
    path = os.path.join(base, fname)
    c = open(path, encoding='utf-8').read()
    if 'admin-mobile-toggle' not in c:
        c = c.replace('</body>', sidebar_js + '\n</body>')
        open(path, 'w', encoding='utf-8').write(c)
        print(f'Added sidebar toggle JS to {fname}')
    else:
        print(f'{fname} already has sidebar toggle')

print("Done!")
