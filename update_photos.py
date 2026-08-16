import glob
import re

html_files = glob.glob(r"d:\Gurudev international\Gurudev intenational\*.html")

address_old = "School Road, Sector 14, Gurugram, Haryana 122001"
address_new = "At Village Kaydi, Tehsil Waraseoni, District Balaghat (M.P.) 481331"

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update the address placeholder
    new_content = content.replace(address_old, address_new)
    
    # 2. Update ALL images in assets/images/ to school_building_main.png 
    # except principal.jpg (or maybe also secretary and director?)
    # Let's replace any assets/images/xxx.jpg with assets/images/school_building_main.png
    
    def replace_image(match):
        img_name = match.group(1)
        # Keep principal or director or chairman photos if they exist
        if 'principal' in img_name.lower() or 'director' in img_name.lower() or 'secretary' in img_name.lower() or 'chairman' in img_name.lower():
            return match.group(0)
        return 'assets/images/school_building_main.png'

    new_content = re.sub(r'assets/images/([^\"\']+)', replace_image, new_content)
    
    # Let's also do replacing of CSS background images if they have any, but we did a blanket replace for HTML.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

print("Address and all photos updated.")
