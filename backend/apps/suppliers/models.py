from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Supplier(models.Model):
    CATEGORY_RAW = 'Raw Materials'
    CATEGORY_ELECTRONICS = 'Electronics'
    CATEGORY_MECHANICAL = 'Mechanical'
    CATEGORY_PACKAGING = 'Packaging'
    CATEGORY_CHEMICALS = 'Chemicals'

    CATEGORY_CHOICES = [
        (CATEGORY_RAW, 'Raw Materials'),
        (CATEGORY_ELECTRONICS, 'Electronics'),
        (CATEGORY_MECHANICAL, 'Mechanical'),
        (CATEGORY_PACKAGING, 'Packaging'),
        (CATEGORY_CHEMICALS, 'Chemicals'),
    ]

    STATUS_ACTIVE = 'Active'
    STATUS_UNDER_REVIEW = 'Under Review'
    STATUS_SUSPENDED = 'Suspended'
    STATUS_INACTIVE = 'Inactive'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_UNDER_REVIEW, 'Under Review'),
        (STATUS_SUSPENDED, 'Suspended'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    supplier_id = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    code = models.CharField(max_length=50, unique=True, db_index=True)
    contact_person = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30)
    address = models.TextField(blank=True, default='')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=CATEGORY_MECHANICAL)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_ACTIVE, db_index=True)
    overall_quality_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return f"{self.name} ({self.code})"

    def recalculate_overall_score(self):
        """Recalculate quality score based on approved reviews."""
        approved_reviews = self.reviews.filter(status='Approved')
        if approved_reviews.exists():
            total = sum(review.overall_score for review in approved_reviews)
            avg_score = round(total / approved_reviews.count(), 2)
            self.overall_quality_score = avg_score
        else:
            self.overall_quality_score = 0.00
        self.save(update_fields=['overall_quality_score', 'updated_at'])
        return self.overall_quality_score

    @property
    def grade(self):
        score = float(self.overall_quality_score)
        if score >= 90:
            return 'A+'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score > 0:
            return 'D'
        return 'N/A'
