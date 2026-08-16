import re
import os

path = r'd:\Gurudev international\Gurudev intenational\css\style.css'
with open(path, 'r', encoding='utf-8') as f:
    css = f.read()

# I will append foolproof CSS for .cse-next and .cse-prev to override everything
foolproof_css = """
/* FOOLPROOF SWIPER ARROWS */
.cseSwiper { position: relative; padding-bottom: 60px !important; }
.cse-next, .cse-prev {
  position: absolute;
  top: 40%;
  transform: translateY(-50%);
  color: white !important;
  background: var(--primary) !important; 
  width: 50px !important; 
  height: 50px !important; 
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0,0,0,0.3); 
  transition: 0.3s;
  z-index: 100 !important;
  display: flex !important;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.cse-prev { left: 10px !important; }
.cse-next { right: 10px !important; }
.cse-next:hover, .cse-prev:hover { background: var(--accent) !important; transform: translateY(-50%) scale(1.1); }
.cse-next i, .cse-prev i { font-size: 1.2rem; }
"""

css += "\n" + foolproof_css

with open(path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css with foolproof arrows")
