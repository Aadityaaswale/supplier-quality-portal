import pytest
from decimal import Decimal
import datetime
from django.contrib.auth.models import User
from apps.suppliers.models import Supplier
from apps.reviews.models import QualityReview


@pytest.mark.django_db
def test_supplier_grade_calculation():
    supplier = Supplier.objects.create(
        supplier_id='SUP-TEST-001',
        name='Test Supplier Precision',
        code='TEST-PREC',
        contact_person='Test Contact',
        email='contact@testprec.com',
        phone='+1234567890',
        category='Electronics',
        status='Active',
        overall_quality_score=Decimal('94.50')
    )
    assert supplier.grade == 'A+'

    supplier.overall_quality_score = Decimal('84.00')
    assert supplier.grade == 'A'

    supplier.overall_quality_score = Decimal('72.00')
    assert supplier.grade == 'B'

    supplier.overall_quality_score = Decimal('55.00')
    assert supplier.grade == 'D'


@pytest.mark.django_db
def test_quality_review_score_calculation():
    user = User.objects.create_user(username='test_reviewer', password='Password123')
    supplier = Supplier.objects.create(
        supplier_id='SUP-TEST-002',
        name='Dynamic Parts Inc',
        code='DYN-PARTS',
        contact_person='Bob Smith',
        email='bob@dynparts.com',
        phone='+1234567899',
        category='Mechanical',
        status='Active'
    )

    review = QualityReview(
        review_id='QR-TEST-001',
        supplier=supplier,
        reviewer=user,
        review_date=datetime.date.today(),
        defect_count=2,
        product_quality_score=Decimal('90.00'),
        compliance_score=Decimal('90.00'),
        delivery_score=Decimal('90.00'),
        status='Draft'
    )
    # Formula: (90 * 0.45) + (90 * 0.30) + (90 * 0.25) - (2 * 0.5) = 90 - 1.0 = 89.00
    calculated = review.calculate_overall_score()
    assert calculated == Decimal('89.00')

    review.save()
    assert review.overall_score == Decimal('89.00')
