import re

path = r'd:\Gurudev international\Gurudev intenational\css\interactive.css'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make Science Lab buttons horizontal on mobile
content = content.replace(
    '.lab-bench-controls { grid-template-columns: 1fr; }',
    '.lab-bench-controls { grid-template-columns: repeat(3, 1fr); gap: 8px; }\n  .lab-btn { padding: 10px 5px; font-size: 0.8rem; flex-direction: column; gap: 4px; }\n  .lab-btn i { font-size: 1.2rem; }'
)

# Enhance Chemistry animation to look more "working"
content = content.replace(
    '.beaker { width: 80px; height: 100px;',
    '.beaker { width: 80px; height: 100px; cursor: pointer;'
)
content = content.replace(
    '.liquid { position: absolute; bottom: 0; left: 0; right: 0; height: 60%; background: #ef4444; border-radius: 0 0 16px 16px; animation: fillUp 1s ease-out; box-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }',
    '.liquid { position: absolute; bottom: 0; left: 0; right: 0; height: 60%; background: #ef4444; border-radius: 0 0 16px 16px; animation: fillUp 1s ease-out, bubbleGlow 2s infinite alternate; box-shadow: 0 0 20px rgba(239, 68, 68, 0.6); }\n@keyframes bubbleGlow { 0% { box-shadow: 0 0 10px rgba(239, 68, 68, 0.4); } 100% { box-shadow: 0 0 30px rgba(239, 68, 68, 0.8); } }'
)

# Enhance Sports Map responsiveness and layout
content = content.replace(
    '.sports-map-visual { min-height: 300px; }',
    '.sports-map-visual { min-height: 250px; aspect-ratio: 4/3; }'
)
content = content.replace(
    '.map-label { font-size: 0.75rem; bottom: -20px; }',
    '.map-label { font-size: 0.65rem; bottom: -15px; background: rgba(255,255,255,0.8); padding: 2px 4px; border-radius: 4px; }'
)

# Make pins bigger on mobile
content = content.replace(
    '.map-pin { font-size: 1.5rem; }',
    '.map-pin { font-size: 1.8rem; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated interactive.css for Science and Sports mobile responsiveness")
