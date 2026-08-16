import os
import glob

html_files = glob.glob('d:/Gurudev international/Gurudev intenational/*.html')

old_html_1 = '<div class="floating-buttons"><a href="https://wa.me/917770822000" class="float-btn float-btn-wa"><i class="fab fa-whatsapp"></i><span class="float-btn-tooltip">WhatsApp</span></a><a href="tel:+917770822000" class="float-btn float-btn-call"><i class="fa-solid fa-phone"></i><span class="float-btn-tooltip">Call</span></a><a href="admission.html" class="float-btn float-btn-adm"><i class="fa-solid fa-star"></i><span class="float-btn-tooltip">Apply</span></a></div>'
old_html_2 = '<div class="floating-buttons">\n  <a href="https://wa.me/917770822000" class="float-btn float-btn-wa"><i class="fab fa-whatsapp"></i><span class="float-btn-tooltip">WhatsApp</span></a>\n  <a href="tel:+917770822000" class="float-btn float-btn-call"><i class="fa-solid fa-phone"></i><span class="float-btn-tooltip">Call</span></a>\n  <a href="admission.html" class="float-btn float-btn-adm"><i class="fa-solid fa-star"></i><span class="float-btn-tooltip">Apply</span></a>\n</div>'

new_html = """<div class="floating-buttons">
  <div class="floating-menu-items">
    <a href="https://wa.me/917770822000" class="float-btn float-btn-wa"><i class="fab fa-whatsapp"></i><span class="float-btn-tooltip">WhatsApp</span></a>
    <a href="tel:+917770822000" class="float-btn float-btn-call"><i class="fa-solid fa-phone"></i><span class="float-btn-tooltip">Call</span></a>
    <a href="admission.html" class="float-btn float-btn-adm"><i class="fa-solid fa-star"></i><span class="float-btn-tooltip">Apply</span></a>
  </div>
  <button class="float-btn float-btn-toggle" aria-label="Contact Options"><i class="fa-solid fa-message"></i></button>
</div>"""

count = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_html_1 in content or old_html_2 in content:
        content = content.replace(old_html_1, new_html)
        content = content.replace(old_html_2, new_html)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1
        
print(f"Updated {count} HTML files.")
