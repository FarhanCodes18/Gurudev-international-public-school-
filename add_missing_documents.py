import re

file_path = r"d:\Gurudev international\Gurudev intenational\mandatory-disclosure.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# For Section B (Documents & Information)
# Find the end of the table rows in Section B
# It ends with:
# <tr><td>8</td><td>Copy of valid DEO Certificate issued by the competent authority</td><td><a href="javascript:void(0);" onclick="alert('Document coming soon')" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
#         </table></div></div>
section_b_additions = """          <tr><td>9</td><td>Certificate of Land</td><td><a href="documnets/CERTIFICATE%20OF%20LAND.pdf" target="_blank" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
          <tr><td>10</td><td>Transport Safety Certificate</td><td><a href="documnets/TRANSPORT%20SAFETY%20CERTIFICATE.pdf" target="_blank" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
          <tr><td>11</td><td>Water Testing Report (Health & Sanitation)</td><td><a href="documnets/WATER%20TESTING%20REPORT.pdf" target="_blank" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
"""

pattern_b = r'(<tr><td>8</td><td>Copy of valid DEO Certificate.*?</tr>\n)'
content = re.sub(pattern_b, r'\1' + section_b_additions, content, count=1)

# For Section C (Result and Academics)
# It ends with:
# <tr><td>5</td><td>Details of Book Store and Dress Store Facilities Available in the Campus</td><td><a href="javascript:void(0);" onclick="alert('Document coming soon')" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
#         </table></div></div>
section_c_additions = """          <tr><td>6</td><td>Assessment & PTM Schedule</td><td><a href="documnets/ASSESSMENT-%20PTM%20SCHEDULE.pdf" target="_blank" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
          <tr><td>7</td><td>Events and Celebration</td><td><a href="documnets/EVENTS%20AND%20CELEBRATION.pdf" target="_blank" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
          <tr><td>8</td><td>Parent Teacher Association (PTA)</td><td><a href="documnets/PARENT%20TEACHER%20ACCOCIATION.pdf" target="_blank" class="doc-link"><i class="fa-solid fa-file-pdf"></i> View Document</a></td></tr>
"""

pattern_c = r'(<tr><td>5</td><td>Details of Book Store.*?</tr>\n)'
content = re.sub(pattern_c, r'\1' + section_c_additions, content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added new rows to mandatory-disclosure.html successfully.")
