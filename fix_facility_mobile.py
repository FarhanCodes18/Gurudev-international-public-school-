import re

path = r'd:\Gurudev international\Gurudev intenational\css\responsive.css'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix .section-header-flex to be centered on tablet/mobile
content = content.replace(
    '.section-header-flex { flex-direction: column; align-items: flex-start; gap: 14px; }',
    '.section-header-flex { flex-direction: column; align-items: center; text-align: center; gap: 16px; }'
)

# 2. Fix the .facility-card height/width issue on mobile (which was restricted by aspect-ratio)
# At 480px:
old_facility_card = '.facility-card   { height: 220px; }'
new_facility_card = '.facility-card   { height: 260px; width: 100%; aspect-ratio: unset; }'
content = content.replace(old_facility_card, new_facility_card)

# Just in case there is any issue at 576px, let's also ensure width 100% there if needed.
# Since 480px overrides 576px, and 576px uses the 3/4 aspect ratio naturally on a 1fr grid,
# the height will scale automatically unless fixed height is set.
# In 576px, we just have grid-template-columns: 1fr; so it scales to 100% width and aspect-ratio maintains height.
# It was only at 480px where I explicitly forced `height: 220px` which broke the width due to aspect-ratio.

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed facility-card width and section-header alignment.")
