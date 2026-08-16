css_to_add = """

/* ====================================================
   MEET OUR FACULTY SECTION
==================================================== */
.faculty-section {
  background: linear-gradient(135deg, #fffdfa 0%, #fef3eb 100%);
  position: relative;
  overflow: hidden;
}

.faculty-slider-wrapper {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 60px;
}

.faculty-slider-container {
  overflow: hidden;
  width: 100%;
}

.faculty-track {
  display: flex;
  gap: 30px;
  transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
  will-change: transform;
}

.faculty-card {
  flex: 0 0 calc(25% - 22.5px); /* 4 cards per row desktop */
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.04);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(0,0,0,0.02);
}

.faculty-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 50px rgba(0,0,0,0.08);
}

.faculty-img-wrapper {
  padding: 15px;
}

.faculty-placeholder {
  width: 100%;
  height: 220px;
  background: linear-gradient(145deg, #d32f2f, #ef4444);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.faculty-placeholder::after {
  content: '\\f007'; /* User icon font-awesome */
  font-family: 'Font Awesome 6 Free';
  font-weight: 900;
  font-size: 4rem;
  color: rgba(255,255,255,0.2);
}

.faculty-info {
  padding: 10px 20px 25px;
  text-align: center;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.faculty-dept {
  color: var(--primary);
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 10px;
}

.faculty-name {
  color: var(--text-dark);
  font-size: 1.25rem;
  font-weight: 800;
  font-family: var(--font-accent);
  margin-bottom: 5px;
}

.faculty-role {
  color: var(--text-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.faculty-qual {
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-bottom: 15px;
  flex: 1;
}

.faculty-socials {
  border-top: 1px solid #f1f5f9;
  padding-top: 15px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

.faculty-socials a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #f8fafc;
  color: #64748b;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.faculty-socials a:hover {
  background: var(--primary);
  color: white;
  transform: translateY(-2px);
}

.faculty-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: white;
  border: 1px solid #e2e8f0;
  color: var(--text-dark);
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  transition: all 0.3s ease;
  z-index: 10;
}

.faculty-arrow:hover {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
  box-shadow: 0 6px 16px rgba(var(--primary-rgb), 0.3);
}

.faculty-arrow.prev { left: 0; }
.faculty-arrow.next { right: 0; }

@media (max-width: 991px) {
  .faculty-card { flex: 0 0 calc(33.333% - 20px); }
  .faculty-slider-wrapper { padding: 0 50px; }
}

@media (max-width: 768px) {
  .faculty-card { flex: 0 0 calc(50% - 15px); }
  .faculty-slider-wrapper { padding: 0 40px; }
}

@media (max-width: 576px) {
  .faculty-card { flex: 0 0 100%; }
  .faculty-slider-wrapper { padding: 0 30px; }
}
"""

with open(r"d:\Gurudev international\Gurudev intenational\css\style.css", "a", encoding="utf-8") as f:
    f.write(css_to_add)

print("CSS added.")
