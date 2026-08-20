import os
import re

file_path = r"d:\Gurudev international\Gurudev intenational\mandatory-disclosure.html"

# Mappings of line prefixes to their new href
# The key is a substring uniquely identifying the row in mandatory-disclosure.html
mappings = {
    "Affiliation/Upgradation letter": "documnets/Affiliation Letter.pdf",
    "Societies/Trust/Company registration": "documnets/GURUDEV SIKHSHAN SAMITI.pdf",
    "No Objection Certificate": "#",
    "Non Proprietary Certificate": "documnets/AFFIDAVIT NON PROPRIETORY.pdf",
    "Recognition Certificate under RTE": "#",
    "Building Safety Certificate": "documnets/BUILDING SAFETY CERTIFICATE.pdf",
    "Fire Safety Certificate": "documnets/FIRE SAFETY CERTIFICATE.pdf",
    "DEO Certificate": "#",
    "Fee Structure of School": "#",
    "Annual Academic Calendar": "documnets/ANNUAL ACADEMIC CALENDAR.pdf",
    "List of School Management Committee": "documnets/SCHOOL MANAGEMENT COMMITTEE.pdf",
    "Last 3-Year Result of the Board": "#",
    "Details of Book Store and Dress Store": "#"
}

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    replaced = False
    for key, doc in mappings.items():
        if key in line:
            # Replace the href link
            if doc == "#":
                line = re.sub(r'href="[^"]+"', r'href="javascript:void(0);" onclick="alert(\'Document coming soon\')"', line)
            else:
                # URL encode spaces in the filename if necessary, but browser handles it mostly
                # Let's replace spaces with %20
                doc_url = doc.replace(" ", "%20")
                line = re.sub(r'href="[^"]+"', f'href="{doc_url}"', line)
            new_lines.append(line)
            replaced = True
            break
    if not replaced:
        new_lines.append(line)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Updated mandatory-disclosure.html successfully.")
