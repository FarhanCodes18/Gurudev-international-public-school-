import re

path = r'd:\Gurudev international\Gurudev intenational\erp-dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the Transport card
card_regex = r'<!-- 5 -->\s*<div class="feature-card border-yellow" onclick="openTransportModal\(\)"[^>]*>.*?</div>\s*</div>'
content = re.sub(card_regex, '<!-- 5 -->\n      <div class="feature-card border-yellow">\n        <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>\n        <div class="text-box">\n          <h3>Transport Routes</h3>\n          <p>Bus & Driver info</p>\n        </div>\n      </div>', content, flags=re.DOTALL)

# Or wait, the user said "hata hi do aap" (just remove it entirely). So remove the card entirely, not just revert it?
# Actually, reverting it to its original non-clickable state is safer, or I can remove the entire card 5.
# If I remove it, the grid goes from 1-4, 6-8. 
# Let's just remove the onclick and modal for now to make it a dead card like it was originally.
# Wait, "transport wala hata hi do aap" implies removing the whole feature.
# Let's remove the card entirely from the dashboard.

card_removal_regex = r'<!-- 5 -->\s*<div class="feature-card border-yellow".*?<h3>Transport Routes</h3>.*?</div>\s*</div>'
content = re.sub(card_removal_regex, '', content, flags=re.DOTALL)


# 2. Remove the modal and script at the bottom
modal_regex = r'<!-- Transport Modal -->.*?</body>'
content = re.sub(modal_regex, '</body>', content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Removed Transport feature from student dashboard.")
