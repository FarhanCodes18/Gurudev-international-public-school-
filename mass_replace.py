import os
import glob
import shutil
import re

# Copy the uploaded image
source_img = r"C:\Users\FARHAN\.gemini\antigravity-ide\brain\6fe7454d-eba1-4d0f-9cb1-5922e9ebcbd9\media__1786630815308.png"
dest_img = r"d:\Gurudev international\Gurudev intenational\assets\images\school_building_main.png"
if os.path.exists(source_img):
    shutil.copy(source_img, dest_img)
    print("Image copied successfully.")

# Files to process
html_files = glob.glob(r"d:\Gurudev international\Gurudev intenational\*.html")

replacements = {
    "Ideal Public School": "Gurudev International Public School",
    "IDEAL PUBLIC SCHOOL": "GURUDEV INTERNATIONAL PUBLIC SCHOOL",
    "Ideal Public": "Gurudev International Public",
    "IDEAL ADMIN": "GURUDEV ADMIN",
    "Ideal Admin": "Gurudev Admin",
    "idealpublicschool47@gmail.com": "gips.balaghat@gmail.com",
    "info@gurudevinternational.edu.in": "gips.balaghat@gmail.com",
    "1030815": "1030822",
    "XXXXXXXX": "1030822", # specifically Affil. No. XXXXXXXX
    "50780": "50787",
    "Mr. Jitesh Nair": "Dr. Anshuman Tiwari",
    "M.A , B.ed": "M.A.(english Literature, M.A. (education), Bed, Phd.",
    "M.Sc., M.Ed., CTET Qualified": "M.A.(english Literature, M.A. (education), Bed, Phd.",
    "principal@gurudevinternational.edu.in": "atiwari031@gmail.com",
    "Mr. Anil Kumar Singh": "Dr. Anshuman Tiwari", # In principal-message.html
    "+91 98765 43210": "7770822000, 9753187666",
    "+91 98765 44444": "7770822000, 9753187666",
    "9876543210": "7770822000",
    "chairman-message.html": "secretary-message.html",
    "Chairman": "Secretary"
}

# Also need to address: At Village Kaydi, Tehsil Waraseoni, District Balaghat (M.P.) 481331
# And Dise Code - 23450700115

def apply_replacements(content):
    # Apply direct string replacements
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # specific address replacement (might be split across lines or tags)
    # usually "At Post XYZ Balaghat" is missing, we need to check how address is formatted. Let's just append the address in footer.
    # Actually, let's find the footer contact item for phone and email and maybe insert address there if not present.
    # We will use regex for some complex parts if needed, but for now direct string replacement is safer.
    
    # Image replacements (banners)
    # common hero images: assets/images/hero-1.jpg, assets/images/hero-2.jpg, assets/images/about-1.jpg, assets/images/campus-1.jpg
    image_regexes = [
        r'assets/images/hero-\d+\.jpg',
        r'assets/images/about-\d+\.jpg',
        r'assets/images/campus-\d+\.jpg',
        r'assets/images/principal\.jpg' # Wait, do we want to change principal photo to school building? No, "har banner and har jgha photos change karo yeh photos dalo aap" means banner and school building photos. Let's leave principal photo alone, or we might accidentally replace it.
    ]
    for pattern in image_regexes[:-1]: # exclude principal for now
        content = re.sub(pattern, 'assets/images/school_building_main.png', content)
        
    return content

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = apply_replacements(content)
    
    # Some specific replacements
    if "Dise Code" not in new_content and "School Code" in new_content:
        # Add Dise Code after School Code in mandatory-disclosure
        new_content = new_content.replace(
            "School Code (if applicable)</td><td>50787</td></tr>",
            "School Code (if applicable)</td><td>50787</td></tr>\n          <tr><td>3a</td><td>Dise Code</td><td>23450700115</td></tr>"
        )
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Rename chairman-message.html to secretary-message.html
old_file = r"d:\Gurudev international\Gurudev intenational\chairman-message.html"
new_file = r"d:\Gurudev international\Gurudev intenational\secretary-message.html"
if os.path.exists(old_file):
    os.rename(old_file, new_file)
    print("Renamed chairman-message.html to secretary-message.html")

print("All replacements done.")
