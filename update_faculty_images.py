import os
import re

file_path = r'd:\Gurudev international\Gurudev intenational\faculty.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to replace all occurrences of 'assets/images/school_building_main.png' inside the faculty carousel with alternating teacher images
teachers = ['teacher-1.jpg', 'teacher-2.jpg', 'teacher-3.jpg', 'teacher-4.jpg']
teacher_index = 0

def replace_func(match):
    global teacher_index
    t = teachers[teacher_index % len(teachers)]
    teacher_index += 1
    return f"assets/images/{t}"

new_content = re.sub(r'assets/images/school_building_main\.png', replace_func, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated images in faculty.html")
