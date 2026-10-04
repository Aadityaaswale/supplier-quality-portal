// Supplier Quality Review Portal - Interactive Features
// Author: AADITYA ASWALE (23102B0044)

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-saas');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });

  // Dynamic Review Score Calculator
  const productQualityInput = document.getElementById('id_product_quality_score');
  const complianceInput = document.getElementById('id_compliance_score');
  const deliveryInput = document.getElementById('id_delivery_score');
  const defectInput = document.getElementById('id_defect_count');
  const scoreDisplay = document.getElementById('computed_overall_score_val');
  const gradeBadge = document.getElementById('computed_grade_badge');

  function calculateScore() {
    if (!productQualityInput || !complianceInput || !deliveryInput || !defectInput) return;

    const pq = parseFloat(productQualityInput.value) || 0;
    const comp = parseFloat(complianceInput.value) || 0;
    const deliv = parseFloat(deliveryInput.value) || 0;
    const defects = parseInt(defectInput.value) || 0;

    // Formula: Product Quality (45%) + Compliance (30%) + Delivery (25%) - (Defects * 0.5)
    const raw = (pq * 0.45) + (comp * 0.30) + (deliv * 0.25);
    const penalty = defects * 0.5;
    const finalScore = Math.max(0.0, Math.min(100.0, raw - penalty)).toFixed(2);

    if (scoreDisplay) {
      scoreDisplay.textContent = finalScore;
    }

    if (gradeBadge) {
      const num = parseFloat(finalScore);
      let grade = 'N/A';
      let badgeClass = 'grade-D';

      if (num >= 90) { grade = 'A+'; badgeClass = 'grade-A-plus'; }
      else if (num >= 80) { grade = 'A'; badgeClass = 'grade-A'; }
      else if (num >= 70) { grade = 'B'; badgeClass = 'grade-B'; }
      else if (num >= 60) { grade = 'C'; badgeClass = 'grade-C'; }
      else if (num > 0) { grade = 'D'; badgeClass = 'grade-D'; }

      gradeBadge.textContent = grade;
      gradeBadge.className = `grade-pill ${badgeClass}`;
    }
  }

  if (productQualityInput) {
    [productQualityInput, complianceInput, deliveryInput, defectInput].forEach(inp => {
      inp.addEventListener('input', calculateScore);
    });
    calculateScore(); // initial run
  }
});
