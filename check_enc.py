import codecs

with codecs.open('css/style.css', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

idx = content.find('footer-link::before')
chunk = content[idx:idx+120]
for c in chunk:
    if ord(c) > 127:
        print(f'SPECIAL CHAR: U+{ord(c):04X} ({repr(c)})')
print('---')
print(repr(chunk))
