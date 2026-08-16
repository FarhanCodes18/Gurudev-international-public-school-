import re

paths = [
    r'd:\Gurudev international\Gurudev intenational\index.html',
    r'd:\Gurudev international\Gurudev intenational\js\achievers-slider.js'
]

for path in paths:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace('color:white; z-index:2;', 'color:white; z-index:2; border-bottom-left-radius:20px; border-bottom-right-radius:20px;')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Updated achiever-info curve.")
