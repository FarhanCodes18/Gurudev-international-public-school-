import re

path = r'd:\Gurudev international\Gurudev intenational\campus.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define mapping from alt text to correct image filename
img_map = {
    'Computer Lab': 'computer_lab.png',
    'Science Lab': 'science_lab.png',
    'Robotics Lab': 'robotics_lab.png',
    'Library': 'library.png',
    'Digital Library': 'library.png', # just in case
    'Sports': 'sports_ground.png',
    'Sports Complex': 'sports_ground.png',
    'Transport': 'school_building_2.png', # since no specific bus image
    'Auditorium': 'auditorium.png',
    'Medical Room': 'school_building_main.png'
}

# The regex looks for an img tag within a facility-card or generally in the facilities-grid.
# Actually, since it's campus.html, let's just find each <img> with alt="..." and replace its src.
def replace_img(match):
    src = match.group(1)
    alt = match.group(2)
    # Check if alt matches our map
    if alt in img_map:
        new_src = f'assets/images/{img_map[alt]}'
        return match.group(0).replace(src, new_src)
    return match.group(0)

# Pattern matches <img src="..." alt="..." ... />
# Actually the HTML might be <img src="assets/images/school_building_main.png" alt="Computer Lab" loading="lazy" />
# Let's use a simpler replacement specifically for facilities-grid
for alt, img_file in img_map.items():
    # Find img tag with this specific alt
    pattern = rf'<img src="assets/images/[^"]+" alt="{alt}"'
    replacement = rf'<img src="assets/images/{img_file}" alt="{alt}"'
    content = re.sub(pattern, replacement, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated images in campus.html!")
