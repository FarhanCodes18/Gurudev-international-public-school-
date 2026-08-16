
import re, os

base = r'd:\Gurudev international\Gurudev intenational'

all_pages = [
    'index.html','about.html','secretary-message.html','director-message.html',
    'principal-message.html','mission-vision.html','campus.html','computer-lab.html',
    'science-lab.html','robotics-lab.html','library.html','sports.html','transport.html',
    'gallery.html','academics.html','e-library.html','admission.html','faculty.html',
    'career.html','services.html','news.html','mandatory-disclosure.html','contact.html',
    'student-portal.html','erp-login.html','erp-register.html','erp-dashboard.html',
    'examination-result.html','notice-board.html','admin-login.html','erp-admin.html',
    'gurudev-super.html',
]

issues = {}

for fname in all_pages:
    path = os.path.join(base, fname)
    if not os.path.exists(path):
        issues[fname] = [f'FILE MISSING']
        continue
    c = open(path, encoding='utf-8').read()
    pg = []

    if 'width=device-width' not in c:
        pg.append('MISSING viewport meta')
    if 'css/responsive.css' not in c:
        pg.append('MISSING responsive.css')

    # Check for bare width:NNNpx (not max-width:) in inline styles
    # Finds: width: 900px but NOT max-width: 900px
    bare_widths = re.findall(r'(?<!max-)(?<!min-)width\s*:\s*(\d+)px', c)
    big = [w for w in bare_widths if int(w) > 600]
    if big:
        pg.append(f'Bare fixed width > 600px: {list(set(big))[:3]}')

    # Tables without scroll container
    if '<table' in c and 'overflow-x' not in c and 'table-responsive' not in c:
        pg.append('Table(s) without scroll container')

    issues[fname] = pg

ok_count = sum(1 for v in issues.values() if not v)
warn_count = sum(1 for v in issues.values() if v)

print(f"\n=== FINAL RESPONSIVE AUDIT — {len(all_pages)} Pages ===\n")
for fname, pg_issues in issues.items():
    if pg_issues:
        print(f"[WARN] {fname}")
        for i in pg_issues:
            print(f"       - {i}")
    else:
        print(f"[PASS] {fname}")

print(f"\n=== RESULT: {ok_count} PASS / {warn_count} WARN ===")
