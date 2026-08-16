import re

def update_faculty():
    path = r'd:\Gurudev international\Gurudev intenational\faculty.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_card = """<div class='faculty-card' data-aos='flip-left' data-aos-duration='1500' style='transform-style: preserve-3d; transition: all 0.5s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer;' onmouseover='this.style.transform="scale(1.08) translateY(-15px) rotateY(10deg)"; this.style.boxShadow="0 25px 50px -12px rgba(0,0,0,0.25)";' onmouseout='this.style.transform="scale(1) translateY(0) rotateY(0deg)"; this.style.boxShadow="";'>
        <div class='faculty-card-img'>
            <img src='farhan done.png' alt='Mohammad Farhan Qureshi' loading='lazy' />
            <div class='faculty-badge'><i class='fa-solid fa-user-tie'></i></div>
        </div>
        <div class='faculty-card-body'>
            <h3 class='faculty-name'>Mohammad Farhan<br>Qureshi</h3>
            <div class='faculty-designation'>IT & Digital Media Manager</div>
            <hr class='faculty-divider'>
            <ul class='faculty-details'>
                <li><i class='fa-regular fa-file-lines'></i> Administration & Tech</li>
                <li><i class='fa-solid fa-graduation-cap'></i> Professional</li>
            </ul>
        </div>
    </div>"""
    
    # Strip line breaks for the regex since the original is on one line
    new_card_single = new_card.replace('\n', '').replace('    ', '')

    new_content = re.sub(r"<div class='faculty-carousel' id='facultyCarousel'>.*?</div><div class='faculty-nav-arrow", "<div class='faculty-carousel' id='facultyCarousel'>" + new_card_single + "</div><div class='faculty-nav-arrow", content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("faculty.html updated")

if __name__ == '__main__':
    update_faculty()
