import os
import glob
import re

html_files = glob.glob('d:/Gurudev international/Gurudev intenational/*.html')

new_html = """<div class="floating-buttons group">
  <div class="floating-menu-items">
    <a href="https://wa.me/917770822000" class="float-btn float-btn-wa" aria-label="WhatsApp Us"><i class="fab fa-whatsapp"></i><span class="float-btn-tooltip">Chat on WhatsApp</span></a>
    <a href="tel:+917770822000" class="float-btn float-btn-call" aria-label="Call us"><i class="fa-solid fa-phone"></i><span class="float-btn-tooltip">Call Now</span></a>
    <a href="admission.html" class="float-btn float-btn-adm" aria-label="Apply for admission"><i class="fa-solid fa-star"></i><span class="float-btn-tooltip">Apply Now</span></a>
  </div>
  <button class="float-btn float-btn-toggle" aria-label="Contact Options"><i class="fa-solid fa-message"></i></button>
</div>"""

count = 0
for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace <div class="floating-buttons"...>...</div> entirely.
    # Because they might have different whitespaces, let's use a robust regex.
    # It starts with <div class="floating-buttons" and ends with </div> before <!-- Back to Top --> or </script> or just the next </div> that contains the 3 a tags.
    
    pattern = re.compile(r'<div class="floating-buttons"[^>]*>.*?</div>', re.DOTALL)
    
    def replacer(match):
        s = match.group(0)
        if 'float-btn-wa' in s and 'float-btn-call' in s and 'float-btn-toggle' not in s:
            return new_html
        return s
    
    new_content = pattern.sub(replacer, content)
    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} HTML files with robust regex.")
