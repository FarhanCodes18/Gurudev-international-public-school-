/* ============================================================
   PARTICLES.JS — Floating Particle Canvas
   ============================================================ */

(function() {
  'use strict';

  class ParticleSystem {
    constructor(canvasId) {
      this.canvas  = document.getElementById(canvasId);
      if (!this.canvas) return;
      this.ctx     = this.canvas.getContext('2d');
      this.particles = [];
      this.count   = 60;
      this.animId  = null;

      this.resize();
      this.createParticles();
      this.animate();

      window.addEventListener('resize', () => this.resize());
    }

    resize() {
      const parent = this.canvas.parentElement;
      this.canvas.width  = parent.offsetWidth;
      this.canvas.height = parent.offsetHeight;
    }

    createParticles() {
      this.particles = [];
      for (let i = 0; i < this.count; i++) {
        this.particles.push(this.newParticle());
      }
    }

    newParticle() {
      return {
        x:     Math.random() * this.canvas.width,
        y:     Math.random() * this.canvas.height,
        r:     Math.random() * 2.5 + 0.5,
        vx:    (Math.random() - 0.5) * 0.4,
        vy:    (Math.random() - 0.5) * 0.4,
        alpha: Math.random() * 0.5 + 0.1,
        color: Math.random() > 0.5
               ? `rgba(212, 175, 55, ${Math.random() * 0.5 + 0.1})`
               : `rgba(255, 255, 255, ${Math.random() * 0.3 + 0.05})`
      };
    }

    drawParticles() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      this.particles.forEach(p => {
        // Draw particle
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        this.ctx.fillStyle = p.color;
        this.ctx.fill();

        // Move
        p.x += p.vx;
        p.y += p.vy;

        // Wrap around edges
        if (p.x < -10) p.x = this.canvas.width + 10;
        if (p.x > this.canvas.width + 10) p.x = -10;
        if (p.y < -10) p.y = this.canvas.height + 10;
        if (p.y > this.canvas.height + 10) p.y = -10;
      });

      // Draw connecting lines between close particles
      for (let i = 0; i < this.particles.length; i++) {
        for (let j = i + 1; j < this.particles.length; j++) {
          const dx   = this.particles[i].x - this.particles[j].x;
          const dy   = this.particles[i].y - this.particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 120) {
            this.ctx.beginPath();
            this.ctx.strokeStyle = `rgba(212, 175, 55, ${0.08 * (1 - dist / 120)})`;
            this.ctx.lineWidth   = 0.5;
            this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
            this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
            this.ctx.stroke();
          }
        }
      }
    }

    animate() {
      this.drawParticles();
      this.animId = requestAnimationFrame(() => this.animate());
    }

    destroy() {
      cancelAnimationFrame(this.animId);
    }
  }

  // Init hero particles
  new ParticleSystem('particle-canvas');

  window.ParticleSystem = ParticleSystem;

})();
