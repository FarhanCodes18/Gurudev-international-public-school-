import re

path = r'd:\Gurudev international\Gurudev intenational\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Regex to match the faculty section completely
# It starts with <section class="faculty-section... and ends with the corresponding </section>
pattern = r'<section class="faculty-section.*?</section>'
new_content = re.sub(pattern, '', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Faculty section removed.")
