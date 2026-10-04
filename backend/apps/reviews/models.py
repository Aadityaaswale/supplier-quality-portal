from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.suppliers.models import Supplier
from decimal import Decimal


class QualityReview(models.Model):
    STATUS_DRAFT = 'Draft'
    STATUS_PENDING_REVIEW = 'Pending Review'
    STATUS_UNDER_REVIEW = 'Under Review'
    STATUS_APPROVED = 'Approved'
    STATUS_REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PENDING_REVIEW, 'Pending Review'),
        (STATUS_UNDER_REVIEW, 'Under Review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    review_id = models.CharField(max_length=50, unique=True, db_index=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quality_reviews')
    review_date = models.DateField()
    defect_count = models.PositiveIntegerField(default=0)
    compliance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    delivery_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    product_quality_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    overall_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        db_index=True
    )
    comments = models.TextField(blank=True, default='')
    manager_remarks = models.TextField(blank=True, default='')
    reviewed_by_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_reviews'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Quality Review'
        verbose_name_plural = 'Quality Reviews'

    def __str__(self):
        return f"{self.review_id} - {self.supplier.name} ({self.status})"

    def calculate_overall_score(self):
        """
        Industry-standard weighted scoring formula:
        - Product Quality: 45%
        - Compliance: 30%
        - Delivery: 25%
        - Defect Penalty: -0.5 points per defective unit (clamped between 0 and 100)
        """
        pq = float(self.product_quality_score or 0)
        comp = float(self.compliance_score or 0)
        deliv = float(self.delivery_score or 0)
        defects = int(self.defect_count or 0)

        raw = (pq * 0.45) + (comp * 0.30) + (deliv * 0.25)
        penalty = defects * 0.5
        final = max(0.0, min(100.0, raw - penalty))
        return Decimal(str(round(final, 2)))

    def save(self, *args, **kwargs):
        self.overall_score = self.calculate_overall_score()
        super().save(*args, **kwargs)
        # Trigger supplier score update if approved
        if self.status == self.STATUS_APPROVED:
            self.supplier.recalculate_overall_score()


class ReviewAuditLog(models.Model):
    ACTION_CREATED = 'CREATED'
    ACTION_UPDATED = 'UPDATED'
    ACTION_SUBMITTED = 'SUBMITTED'
    ACTION_UNDER_REVIEW = 'UNDER_REVIEW'
    ACTION_APPROVED = 'APPROVED'
    ACTION_REJECTED = 'REJECTED'

    ACTION_CHOICES = [
        (ACTION_CREATED, 'Created'),
        (ACTION_UPDATED, 'Updated'),
        (ACTION_SUBMITTED, 'Submitted for Approval'),
        (ACTION_UNDER_REVIEW, 'Moved to Under Review'),
        (ACTION_APPROVED, 'Approved'),
        (ACTION_REJECTED, 'Rejected'),
    ]

    review = models.ForeignKey(QualityReview, on_delete=models.CASCADE, related_name='audit_logs')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    old_status = models.CharField(max_length=30, blank=True, default='')
    new_status = models.CharField(max_length=30, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Review Audit Log'
        verbose_name_plural = 'Review Audit Logs'

    def __str__(self):
        return f"{self.review.review_id} - {self.action} by {self.actor} at {self.timestamp}"
