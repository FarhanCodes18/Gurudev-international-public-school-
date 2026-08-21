import re

with open('management-committee.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update Title and breadcrumb
html = html.replace('Principal\'s Message</title>', 'Management Committee | Gurudev International Public School</title>')
html = html.replace('<h1 class="page-hero-title" data-aos="fade-down">Principal\'s Message</h1>', '<h1 class="page-hero-title" data-aos="fade-down">Our Visionaries</h1>')
html = html.replace('<span class="breadcrumb-item active">Principal\'s Message</span>', '<span class="breadcrumb-item active">Management Committee</span>')

# Define the members
members = [
    {
        'name': 'Mr. Ravi Meghe',
        'designation': 'Vice President',
        'org': 'Gurudev Shikshan Samiti',
        'image': 'assets/images/ravi meghe.png',
        'quote': 'Education is the most powerful weapon which you can use to change the world.',
        'msg': 'We are committed to providing an environment where every student is empowered to discover their true potential. Our focus remains on holistic development and academic excellence.'
    },
    {
        'name': 'Mr. Chandrakant Tiwari',
        'designation': 'Treasurer',
        'org': 'Gurudev Shikshan Samiti',
        'image': 'assets/images/chandrakant tiwari.png',
        'quote': 'Integrity, transparency, and dedication are the pillars of a successful educational institution.',
        'msg': 'Our goal is to ensure that the resources of this institution are utilized effectively to provide world-class facilities, fostering an atmosphere conducive to modern learning.'
    },
    {
        'name': 'Mr. Thanendra Turkar',
        'designation': 'Secretary',
        'org': 'Gurudev Shikshan Samiti',
        'image': 'assets/images/turkar.png',
        'quote': 'A school is a building surrounded by four walls with the future inside.',
        'msg': 'We envision Gurudev International Public School as a beacon of knowledge and character building. We strive to instill core values that help students navigate the complexities of tomorrow.'
    },
    {
        'name': 'Mrs. Madhuri Meghe',
        'designation': 'Joint Secretary',
        'org': 'Gurudev Shikshan Samiti',
        'image': 'assets/images/Madhuri Meghe.png',
        'quote': 'Empowering students to think critically and act compassionately is our true mission.',
        'msg': 'Education should inspire innovation and kindness alike. I am proud to be part of a team that continuously works towards creating a nurturing and inclusive environment for all students.'
    },
    {
        'name': 'Mr. Harshit Turkar',
        'designation': 'Executive Board Member',
        'org': 'Gurudev Shikshan Samiti',
        'image': 'assets/images/harshit.png',
        'quote': 'The future belongs to those who believe in the beauty of their dreams.',
        'msg': 'By integrating modern technology and innovative teaching methodologies, we aim to prepare our students to face global challenges with confidence and resilience.'
    },
    {
        'name': 'Mrs. Aparna Tiwari',
        'designation': 'Executive Board Member',
        'org': 'Gurudev Shikshan Samiti',
        'image': 'assets/images/aparna tiwari.png',
        'quote': 'Nurturing curiosity today leads to the innovations of tomorrow.',
        'msg': 'We focus on ensuring that our curriculum and extracurricular activities are balanced, giving every child the opportunity to explore their interests and excel in their chosen paths.'
    }
]

sections_html = ""
for i, member in enumerate(members):
    img_col = f'''<div style="background:var(--secondary);border-radius:var(--radius-xl);overflow:hidden;box-shadow:var(--shadow-lg);border:1px solid var(--border-color)" data-aos="{'fade-right' if i%2==0 else 'fade-left'}">
  <div style="background:linear-gradient(135deg,var(--primary-dark),var(--primary));padding:40px 30px;text-align:center">
    <img src="{member['image']}" alt="{member['name']}" style="width:240px;height:240px;border-radius:16px;border:4px solid var(--accent);object-fit:cover;margin:0 auto 16px;display:block;box-shadow:0 8px 30px rgba(0,0,0,.3)" loading="lazy" />
    <div style="font-family:var(--font-accent);font-size:1.2rem;font-weight:800;color:var(--secondary)">{member['name']}</div>
    <div style="font-size:.82rem;color:var(--accent);text-transform:uppercase;letter-spacing:1px">{member['designation']}</div>
    <div style="font-size:.75rem;color:var(--secondary);margin-top:4px;">{member['org']}</div>
  </div>
</div>'''

    text_col = f'''<div data-aos="{'fade-left' if i%2==0 else 'fade-right'}">
  <div class="section-label">Message from the {member['designation']}</div>
  <h2 class="section-title">{member['name']}</h2>
  <blockquote style="border-left:4px solid var(--accent);padding:16px 24px;background:rgba(212,175,55,.06);border-radius:0 var(--radius-md) var(--radius-md) 0;font-style:italic;color:var(--text-secondary);margin:24px 0;font-size:1.05rem;line-height:1.8">"{member['quote']}"</blockquote>
  <p style="font-size:.95rem;color:var(--text-secondary);line-height:1.95;margin-bottom:18px">{member['msg']}</p>
  <div style="font-family:Georgia,serif;font-size:1.6rem;color:var(--primary);margin-top:32px;font-style:italic">{member['name']}</div>
  <p style="color:var(--text-muted);font-size:.85rem;margin-top:8px">{member['designation']}, {member['org']}</p>
</div>'''

    if i % 2 == 0:
        row = f'<div style="display:grid;grid-template-columns:340px 1fr;gap:60px;align-items:start;margin-bottom:80px;">\n{img_col}\n{text_col}\n</div>'
    else:
        row = f'''<div style="display:flex; flex-wrap:wrap-reverse; gap:60px; align-items:start; margin-bottom:80px;">
  <div style="flex:1; min-width:300px;">
    {text_col}
  </div>
  <div style="width:340px; max-width:100%;">
    {img_col}
  </div>
</div>'''
    
    sections_html += row

# Now replace the principal's section with all sections
# The previous principal section is contained inside <div style="display:grid;grid-template-columns:340px 1fr;gap:60px;align-items:start"> ... </div></div>
# We can search for <div style="display:grid;grid-template-columns:340px 1fr;gap:60px;align-items:start"> and ending just before </section>
pattern = r'<div style="display:grid;grid-template-columns:340px 1fr;gap:60px;align-items:start">.*?(?=\s*</div></section>)'
html = re.sub(pattern, sections_html, html, flags=re.DOTALL)

with open('management-committee.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated management-committee.html successfully.")
