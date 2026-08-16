
import re, os

base = r'd:\Gurudev international\Gurudev intenational'

# More aggressive inline width fixer using proper regex
def fix_all_inline_widths(content, fname):
    changes = 0

    # Pattern: style="...width: 700px..." or style='...'
    # Replace large fixed widths with max-width + 100%
    def sub_width(m):
        nonlocal changes
        full_style = m.group(0)
        # Find width:NNNpx inside the style attribute
        def replace_w(wm):
            nonlocal changes
            px = int(wm.group(1))
            if px > 600:
                changes += 1
                return f'width:100%;max-width:{px}px'
            return wm.group(0)
        new_style = re.sub(r'width\s*:\s*(\d+)px', replace_w, full_style)
        return new_style

    result = re.sub(r'style=["\'][^"\']{1,300}["\']', sub_width, content)
    if changes:
        print(f'  Fixed {changes} inline width(s) in {fname}')
    return result

pages = ['index.html', 'admission.html', 'career.html', 'erp-dashboard.html', 'gurudev-super.html']

for fname in pages:
    path = os.path.join(base, fname)
    c = open(path, encoding='utf-8').read()
    c2 = fix_all_inline_widths(c, fname)
    if c2 != c:
        open(path, 'w', encoding='utf-8').write(c2)
    else:
        print(f'  No more changes for {fname}')

print("Done!")
