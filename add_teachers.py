import re

html_path = r"d:\Projects\Gurudev intenational\faculty.html"

teachers = [
    {"name": "Mr. Ajay Garg", "desig": "Assistant Professor", "subject": "Deep Learning", "degree": "M.Tech", "img": "teacher-1.jpg"},
    {"name": "Mr. Deepak<br>Kumar Thakur", "desig": "Assistant Professor", "subject": "Machine Learning", "degree": "MCA", "img": "teacher-2.jpg"},
    {"name": "Mr. Nikesh<br>Sharnagat", "desig": "Lecturer", "subject": "Web Development", "degree": "M.Tech", "img": "teacher-3.jpg"},
    {"name": "Mr. Bhavesh<br>Goswami", "desig": "Lecturer", "subject": "C++", "degree": "B.Tech", "img": "teacher-4.jpg"},
    {"name": "Ms. Priya<br>Sharma", "desig": "Senior Professor", "subject": "Data Science", "degree": "Ph.D", "img": "teacher-1.jpg"},
    {"name": "Mr. Rajesh<br>Kumar", "desig": "Assistant Professor", "subject": "Artificial Intelligence", "degree": "M.Tech", "img": "teacher-2.jpg"},
    {"name": "Mrs. Sunita<br>Verma", "desig": "Lecturer", "subject": "Software Engineering", "degree": "M.Tech", "img": "teacher-3.jpg"},
    {"name": "Mr. Amit<br>Singh", "desig": "Assistant Professor", "subject": "Cyber Security", "degree": "MCA", "img": "teacher-4.jpg"},
    {"name": "Ms. Neha<br>Gupta", "desig": "Lecturer", "subject": "Cloud Computing", "degree": "B.Tech", "img": "teacher-1.jpg"},
    {"name": "Mr. Vikram<br>Patel", "desig": "Assistant Professor", "subject": "Database Systems", "degree": "M.Tech", "img": "teacher-2.jpg"},
    {"name": "Mrs. Anjali<br>Desai", "desig": "Associate Professor", "subject": "Computer Networks", "degree": "M.Tech", "img": "teacher-3.jpg"},
    {"name": "Mr. Rahul<br>Jain", "desig": "Lecturer", "subject": "Operating Systems", "degree": "MCA", "img": "teacher-4.jpg"},
    {"name": "Ms. Kavita<br>Reddy", "desig": "Lecturer", "subject": "Mobile App Dev", "degree": "B.Tech", "img": "teacher-1.jpg"},
    {"name": "Mr. Suresh<br>Menon", "desig": "Assistant Professor", "subject": "Computer Graphics", "degree": "M.Tech", "img": "teacher-2.jpg"},
    {"name": "Mrs. Meera<br>Joshi", "desig": "Lecturer", "subject": "Data Structures", "degree": "MCA", "img": "teacher-3.jpg"}
]

cards_html = ""
for t in teachers:
    cards_html += f"""<div class='faculty-card'><div class='faculty-card-img'><img src='assets/images/{t['img']}' alt='{t['name'].replace('<br>', ' ')}' loading='lazy' /><div class='faculty-badge'><i class='fa-solid fa-user-tie'></i></div></div><div class='faculty-card-body'><h3 class='faculty-name'>{t['name']}</h3><div class='faculty-designation'>{t['desig']}</div><hr class='faculty-divider'><ul class='faculty-details'><li><i class='fa-regular fa-file-lines'></i> {t['subject']}</li><li><i class='fa-solid fa-graduation-cap'></i> {t['degree']}</li></ul></div></div>"""

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the inner content of the carousel
pattern = r"(<div class='faculty-carousel' id='facultyCarousel'>).*?(</div><div class='faculty-nav-arrow faculty-nav-left' id='facultyPrev'>)"
new_content = re.sub(pattern, rf"\g<1>{cards_html}\g<2>", content, flags=re.DOTALL)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Added {len(teachers)} teachers to faculty.html")
