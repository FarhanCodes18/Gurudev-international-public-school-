import re
import os

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'robotics-lab.html')

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

interactive_html = """
  <!-- INTERACTIVE ROBOTICS TERMINAL -->
  <section class="section-padding interactive-section" id="robot-terminal" style="background:var(--bg-dark); color:white;">
    <div class="container">
      <div class="section-header">
        <div class="section-label">Interactive Coding</div>
        <h2 class="section-title text-white">Code &amp; <span>Control</span></h2>
        <p class="section-subtitle text-white" style="opacity:0.7;">Write commands to control the virtual robot.</p>
      </div>

      <div class="robot-workspace">
        <!-- Terminal Side -->
        <div class="robot-terminal-panel">
          <div class="terminal-header">
            <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
            <div class="terminal-title">bash - robotics_control</div>
          </div>
          <div class="terminal-body">
            <div class="terminal-line"><span class="prompt">user@gips:~$</span> ./init_robot.sh</div>
            <div class="terminal-line sys">Robot initialized. Awaiting commands...</div>
            <div class="terminal-line"><span class="prompt">user@gips:~$</span> <span id="typing-command" class="typing-text"></span></div>
          </div>
          <div class="terminal-controls">
            <button class="cmd-btn" data-cmd="boot">Boot Up</button>
            <button class="cmd-btn" data-cmd="move">Move Arms</button>
            <button class="cmd-btn" data-cmd="scan">Scan Area</button>
            <button class="cmd-btn" data-cmd="shutdown">Shutdown</button>
          </div>
        </div>

        <!-- Robot Side -->
        <div class="robot-display-panel">
          <div class="css-robot" id="virtual-bot">
            <div class="bot-head">
              <div class="bot-eye left"></div>
              <div class="bot-eye right"></div>
            </div>
            <div class="bot-body">
              <div class="bot-screen">
                <div class="heartbeat-line"></div>
              </div>
            </div>
            <div class="bot-arm left"></div>
            <div class="bot-arm right"></div>
            <div class="bot-wheels">
              <div class="wheel"></div>
              <div class="wheel"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# Insert before admission-banner
if 'id="robot-terminal"' not in content:
    content = content.replace(
        '<section class="admission-banner',
        interactive_html + '\n  <section class="admission-banner'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected Robotics Terminal into robotics-lab.html")
else:
    print("Robotics Terminal already exists in robotics-lab.html")
