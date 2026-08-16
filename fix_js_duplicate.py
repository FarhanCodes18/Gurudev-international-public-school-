import os
import re

path = r'd:\Gurudev international\Gurudev intenational\js\erp-student.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Transport Routes module block and remove it completely
transport_module_regex = r"""    \{\s*selector: '\.feature-card:nth-child\(5\)',\s*title: 'Transport Routes',\s*render: \(\) => emptyState\('fa-solid fa-bus-simple', 'No Route Assigned', 'You are not assigned to any school transport route\. Please contact the transport admin\.'\)\s*\},"""

new_content = re.sub(transport_module_regex, '', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Removed duplicate Transport Routes module from erp-student.js.")
