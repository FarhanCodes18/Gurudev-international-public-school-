
import os, re

base = r'd:\Gurudev international\Gurudev intenational'

# ─────────────────────────────────────────────────────────────────────
# 1. ALL pages that are missing responsive.css — inject it
# ─────────────────────────────────────────────────────────────────────
pages_missing_resp = [
    'e-library.html',
    'erp-admin.html',
    'erp-dashboard.html',
    'erp-login.html',
    'erp-register.html',
    'examination-result.html',
    'notice-board.html',
]

pages_missing_style = [
    'admin-login.html',
    'gurudev-super.html',
]

for fname in pages_missing_resp:
    path = os.path.join(base, fname)
    c = open(path, encoding='utf-8').read()
    if 'css/responsive.css' not in c:
        # Insert before </head>
        c = c.replace('</head>', '<link rel="stylesheet" href="css/responsive.css" />\n</head>', 1)
        open(path, 'w', encoding='utf-8').write(c)
        print(f'Added responsive.css to {fname}')

for fname in pages_missing_style:
    path = os.path.join(base, fname)
    c = open(path, encoding='utf-8').read()
    changes = False
    if 'css/style.css' not in c and 'css/admin.css' not in c:
        # For admin-login, it has its own inline styles, just add responsive
        pass
    if 'css/responsive.css' not in c:
        c = c.replace('</head>', '<link rel="stylesheet" href="css/responsive.css" />\n</head>', 1)
        open(path, 'w', encoding='utf-8').write(c)
        print(f'Added responsive.css to {fname}')

print("Phase 1 done: responsive.css injected into all missing pages")
