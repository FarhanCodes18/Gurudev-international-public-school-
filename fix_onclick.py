import os

path = r'd:\Gurudev international\Gurudev intenational\erp-dashboard.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# I will use a more robust replacement strategy.
# Let's find the exact string segment
old_str = '<div class="feature-card border-yellow">\n          <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>\n          <div class="text-box">\n            <h3>Transport Routes</h3>\n            <p>Bus & Driver info</p>\n          </div>'
new_str = '<div class="feature-card border-yellow" onclick="openTransportModal()" style="cursor:pointer;">\n          <div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>\n          <div class="text-box">\n            <h3>Transport Routes</h3>\n            <p>Bus & Driver info</p>\n          </div>'

if 'onclick="openTransportModal()"' not in content:
    # Let's just do a manual replace of just the div containing the bus icon since there are multiple border-yellow cards
    lines = content.split('\n')
    for i in range(len(lines)):
        if '<div class="icon-box bg-yellow-light text-yellow"><i class="fa-solid fa-bus"></i></div>' in lines[i]:
            # The line above should be the feature-card
            if '<div class="feature-card border-yellow">' in lines[i-1]:
                lines[i-1] = lines[i-1].replace('<div class="feature-card border-yellow">', '<div class="feature-card border-yellow" onclick="openTransportModal()" style="cursor:pointer;">')
                break
    
    content = '\n'.join(lines)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed onclick attribute!")
else:
    print("onclick already present.")
