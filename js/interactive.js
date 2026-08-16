import os

base = r'd:\Gurudev international\Gurudev intenational'
path = os.path.join(base, 'js', 'interactive.js')

js_content = """/* ==========================================================================
   INTERACTIVE ELEMENTS JS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {

  // --------------------------------------------------------------------------
  // 1. SCIENCE VIRTUAL LAB BENCH
  // --------------------------------------------------------------------------
  const labBtns = document.querySelectorAll('.lab-btn');
  if (labBtns.length > 0) {
    labBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        // Remove active class from all buttons
        labBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Hide all screens
        document.querySelectorAll('.lab-screen-content').forEach(screen => {
          screen.classList.add('hidden');
        });
        
        // Show target screen
        const target = btn.getAttribute('data-target');
        const targetScreen = document.getElementById(`lab-screen-${target}`);
        if (targetScreen) {
          targetScreen.classList.remove('hidden');
        }
      });
    });
  }

  // --------------------------------------------------------------------------
  // 2. ROBOTICS TERMINAL & ROBOT
  // --------------------------------------------------------------------------
  const cmdBtns = document.querySelectorAll('.cmd-btn');
  const robot = document.getElementById('virtual-bot');
  const typingCommand = document.getElementById('typing-command');
  
  if (cmdBtns.length > 0 && robot) {
    cmdBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const cmd = btn.getAttribute('data-cmd');
        
        // Type out the command
        typingCommand.textContent = '';
        let i = 0;
        const text = `./execute_${cmd}.sh`;
        const typeInterval = setInterval(() => {
          typingCommand.textContent += text.charAt(i);
          i++;
          if (i >= text.length) {
            clearInterval(typeInterval);
            executeCommand(cmd);
          }
        }, 50);
      });
    });

    function executeCommand(cmd) {
      // Reset classes
      robot.className = 'css-robot';
      
      // Force reflow
      void robot.offsetWidth;
      
      switch(cmd) {
        case 'boot':
          robot.classList.add('booting');
          break;
        case 'move':
          robot.classList.add('booting', 'moving');
          break;
        case 'scan':
          robot.classList.add('booting', 'scanning');
          break;
        case 'shutdown':
          // Just reset classes
          break;
      }
    }
  }

  // --------------------------------------------------------------------------
  // 3. LIBRARY 3D BOOKSHELF
  // --------------------------------------------------------------------------
  const bookContainers = document.querySelectorAll('.book-container');
  if (bookContainers.length > 0) {
    bookContainers.forEach(container => {
      container.addEventListener('click', () => {
        // Toggle flip on click
        const isFlipped = container.classList.contains('flipped');
        
        // Close others
        bookContainers.forEach(c => c.classList.remove('flipped'));
        
        if (!isFlipped) {
          container.classList.add('flipped');
        }
      });
      
      // Close flip when mouse leaves completely
      container.addEventListener('mouseleave', () => {
        setTimeout(() => {
          container.classList.remove('flipped');
        }, 500);
      });
    });
  }

  // --------------------------------------------------------------------------
  // 4. SPORTS INTERACTIVE MAP
  // --------------------------------------------------------------------------
  const mapFields = document.querySelectorAll('.map-field');
  if (mapFields.length > 0) {
    mapFields.forEach(field => {
      field.addEventListener('click', () => {
        // Active state on map
        mapFields.forEach(f => f.classList.remove('active'));
        field.classList.add('active');
        
        // Show info card
        document.querySelectorAll('.sports-info-card').forEach(card => {
          card.classList.add('hidden');
        });
        
        const zone = field.getAttribute('data-zone');
        const targetCard = document.getElementById(`sports-info-${zone}`);
        if (targetCard) {
          targetCard.classList.remove('hidden');
        }
      });
    });
  }

});
"""

with open(path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Created interactive.js")
