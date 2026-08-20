import os
import re

base_path = r"d:\Gurudev international\Gurudev intenational"

file_replacements = {
    'computer-lab.html': [
        (r'<img src=[\'"]assets/images/school_building_main.png[\'"]\s+alt=[\'"]Computer Lab[\'"]', r'<img src="assets/images/computer_lab.png" alt="Computer Lab"')
    ],
    'library.html': [
        (r'<img src=[\'"]assets/images/school_building_main.png[\'"]\s+alt=[\'"]Library[\'"]', r'<img src="assets/images/library.png" alt="Library"')
    ],
    'robotics-lab.html': [
        (r'<img src=[\'"]assets/images/school_building_main.png[\'"]\s+alt=[\'"]Robotics Lab[\'"]', r'<img src="assets/images/robotics_lab.png" alt="Robotics Lab"')
    ],
    'science-lab.html': [
        (r'<img src=[\'"]assets/images/school_building_main.png[\'"]\s+alt=[\'"]Science Lab[\'"]', r'<img src="assets/images/science_lab.png" alt="Science Lab"')
    ],
    'sports.html': [
        (r'<img src=[\'"]assets/images/school_building_main.png[\'"]\s+alt=[\'"]Sports[\'"]', r'<img src="assets/images/sports_ground.png" alt="Sports"')
    ],
    'transport.html': [
        (r'<img src=[\'"]assets/images/school_building_main.png[\'"]\s+alt=[\'"]Transport[\'"]', r'<img src="assets/images/school_building_2.png" alt="Transport"')
    ]
}

img_map = {
    'Computer Lab': 'computer_lab.png',
    'Science Lab': 'science_lab.png',
    'Robotics Lab': 'robotics_lab.png',
    'Library': 'library.png',
    'Sports': 'sports_ground.png',
    'Transport': 'school_building_2.png',
    'Auditorium': 'auditorium.png',
    'Arts & Music': 'arts_music.png',
    'Science lab': 'science_lab.png'
}

def update_file(filepath):
    if not os.path.exists(filepath):
        return
        
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    if filename in file_replacements:
        for old_pattern, new_text in file_replacements[filename]:
            content = re.sub(old_pattern, new_text, content)
            
    for alt, img_file in img_map.items():
        pattern1 = rf'<img[^>]*src=[\'"]assets/images/school_building_main.png[\'"][^>]*alt=[\'"]{alt}[\'"]'
        def repl1(match):
            m = match.group(0)
            return m.replace('school_building_main.png', img_file)
        
        content = re.sub(pattern1, repl1, content)
        
        pattern2 = rf'<img[^>]*alt=[\'"]{alt}[\'"][^>]*src=[\'"]assets/images/school_building_main.png[\'"]'
        def repl2(match):
            m = match.group(0)
            return m.replace('school_building_main.png', img_file)
            
        content = re.sub(pattern2, repl2, content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated images in {filename}")

for filename in file_replacements.keys():
    update_file(os.path.join(base_path, filename))

update_file(os.path.join(base_path, 'index.html'))
update_file(os.path.join(base_path, 'campus.html'))

if os.path.exists(os.path.join(base_path, 'e-library.html')):
    update_file(os.path.join(base_path, 'e-library.html'))
