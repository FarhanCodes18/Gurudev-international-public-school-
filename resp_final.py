
import re, os

base = r'd:\Gurudev international\Gurudev intenational'

# ─────────────────────────────────────────────────────────────────────
# Fix 1: Replace fixed inline widths > 600px with max-width + width:100%
# ─────────────────────────────────────────────────────────────────────
def fix_inline_widths(content):
    """Replace inline style width:NNNpx (>600) with max-width:NNNpx; width:100%"""
    def replacer(m):
        full = m.group(0)
        px_val = int(m.group(1))
        if px_val > 600:
            fixed = full.replace(f'width:{px_val}px', f'width:100%;max-width:{px_val}px')
            fixed = fixed.replace(f'width: {px_val}px', f'width:100%;max-width:{px_val}px')
            return fixed
        return full
    return re.sub(r'style=["\'][^"\']*width\s*:\s*(\d+)px[^"\']*["\']', replacer, content)

# ─────────────────────────────────────────────────────────────────────
# Fix 2: Wrap bare <table> tags with scroll container if not already wrapped
# ─────────────────────────────────────────────────────────────────────
def wrap_tables(content):
    """Wrap tables not already inside .table-scroll-wrap or overflow-x:auto container"""
    # Pattern: find <table that isn't preceded by table-scroll-wrap within 200 chars
    result = content
    tables = list(re.finditer(r'(?<!table-responsive[^<]{0,100})<table(?!\s*class="[^"]*responsive)', content))
    # Simpler approach: check if tables are already wrapped
    if 'table-scroll-wrap' not in content and 'overflow-x' not in content:
        result = re.sub(r'(<table\b)', r'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">\1', content)
        result = re.sub(r'(</table>)', r'\1</div>', result)
    return result

# ─────────────────────────────────────────────────────────────────────
# Apply fixes to flagged pages
# ─────────────────────────────────────────────────────────────────────

# Fix inline widths
width_pages = ['index.html', 'admission.html', 'career.html', 'erp-dashboard.html', 'gurudev-super.html']
for fname in width_pages:
    path = os.path.join(base, fname)
    c = open(path, encoding='utf-8').read()
    c2 = fix_inline_widths(c)
    if c2 != c:
        open(path, 'w', encoding='utf-8').write(c2)
        print(f'Fixed inline widths in {fname}')
    else:
        print(f'No change needed for {fname}')

# Fix table wrapping for pages with bare tables
table_pages = ['mandatory-disclosure.html', 'examination-result.html']
for fname in table_pages:
    path = os.path.join(base, fname)
    c = open(path, encoding='utf-8').read()
    # Check if already has overflow-x in context
    if 'overflow-x' not in c and 'table-responsive' not in c:
        c2 = re.sub(r'(<table\b)', r'<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;width:100%;">\1', c)
        c2 = re.sub(r'(</table>)', r'\1</div>', c2)
        open(path, 'w', encoding='utf-8').write(c2)
        print(f'Wrapped tables in {fname}')
    else:
        print(f'{fname} already has scroll wrapper')

# ─────────────────────────────────────────────────────────────────────
# Fix 3: Add global overflow-x prevention to style.css root level
# ─────────────────────────────────────────────────────────────────────
style_path = os.path.join(base, 'css', 'style.css')
style = open(style_path, encoding='utf-8').read()
global_fix = """
/* ============================================================
   GLOBAL RESPONSIVE BASE — OVERFLOW PREVENTION
   ============================================================ */
html {
  overflow-x: clip;
}
body {
  max-width: 100vw;
  overflow-x: hidden;
}
img, video, iframe, canvas, svg, embed, object {
  max-width: 100%;
}
*, *::before, *::after {
  box-sizing: border-box;
}
"""
if 'GLOBAL RESPONSIVE BASE' not in style:
    # Insert right after the :root block closes
    style = style + '\n' + global_fix
    open(style_path, 'w', encoding='utf-8').write(style)
    print("Added global overflow fix to style.css")

# ─────────────────────────────────────────────────────────────────────
# Fix 4: Ensure erp-dashboard max-width is responsive
# ─────────────────────────────────────────────────────────────────────
erp_dash = os.path.join(base, 'erp-dashboard.html')
c = open(erp_dash, encoding='utf-8').read()
# Replace the inline max-width:1200px container with responsive version
c = c.replace("style=\"max-width: 1200px;\"", "style=\"max-width:min(1200px,100%); padding:0 clamp(12px,3vw,24px);\"")
open(erp_dash, 'w', encoding='utf-8').write(c)
print("Fixed erp-dashboard container width")

print("\nAll fixes complete!")
