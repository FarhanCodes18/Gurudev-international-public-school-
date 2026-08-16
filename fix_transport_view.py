import os

path = r'd:\Gurudev international\Gurudev intenational\gurudev-super.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_start = '<div class="admin-view" id="view-transport" style="display:none;">'
new_start = '<section id="view-transport" class="view-section">'

if old_start in content:
    content = content.replace(old_start, new_start)

# Since I just replaced the start, I need to find the specific closing div and replace it with section.
# The transport view ends right before </main>
old_end = """          </div>
        </div>

      </main>"""
new_end = """          </div>
        </section>

      </main>"""

if old_end in content:
    content = content.replace(old_end, new_end)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed view-transport HTML structure.")
