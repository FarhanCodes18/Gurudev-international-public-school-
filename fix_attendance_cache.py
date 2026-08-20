import re

# 1. Update erp-dashboard.html version string
html_path = r"d:\Gurudev international\Gurudev intenational\erp-dashboard.html"
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

html_content = html_content.replace('src="js/erp-student.js?v=2"', 'src="js/erp-student.js?v=3"')
html_content = html_content.replace('src="js/erp-student.js"', 'src="js/erp-student.js?v=3"') # In case it didn't have v=2

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)


# 2. Update erp-student.js to also exclude Sunday and make sure we didn't miss it
js_path = r"d:\Gurudev international\Gurudev intenational\js\erp-student.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Update the if statement in erp-student.js
old_if = "if(status !== 'Holiday') {"
new_if = "if(status !== 'Holiday' && status !== 'Sunday') {"

if old_if in js_content:
    js_content = js_content.replace(old_if, new_if)
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Fixed JS logic and bumped version.")
else:
    print("Could not find the if statement in JS. Maybe it's already updated.")
