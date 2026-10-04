import pytest
from decimal import Decimal
import datetime
from django.contrib.auth.models import User
from apps.suppliers.models import Supplier
from apps.reviews.models import QualityReview
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_review_status_transition_workflow():
    client = APIClient()

    reviewer = User.objects.create_user(username='rev1', password='Password123')
    reviewer.profile.role = 'REVIEWER'
    reviewer.profile.save()

    manager = User.objects.create_user(username='mgr1', password='Password123')
    manager.profile.role = 'QUALITY_MANAGER'
    manager.profile.save()

    supplier = Supplier.objects.create(
        supplier_id='SUP-WF-001',
        name='Workflow Components',
        code='WF-COMP',
        contact_person='Alice',
        email='alice@wf.com',
        phone='111222333',
        category='Electronics',
        status='Active'
    )

    review = QualityReview.objects.create(
        review_id='QR-WF-001',
        supplier=supplier,
        reviewer=reviewer,
        review_date=datetime.date.today(),
        defect_count=0,
        product_quality_score=Decimal('95.00'),
        compliance_score=Decimal('95.00'),
        delivery_score=Decimal('95.00'),
        status=QualityReview.STATUS_DRAFT
    )

    # 1. Reviewer submits review: Draft -> Pending Review
    client.force_authenticate(user=reviewer)
    response = client.post(f'/api/reviews/{review.id}/transition/', {'status': 'Pending Review'})
    assert response.status_code == 200
    review.refresh_from_db()
    assert review.status == QualityReview.STATUS_PENDING_REVIEW

    # 2. Reviewer tries to approve own review -> Must fail (403 Forbidden)
    response = client.post(f'/api/reviews/{review.id}/transition/', {'status': 'Approved', 'notes': 'Trying to self-approve'})
    assert response.status_code == 403

    # 3. Quality Manager approves review -> Must succeed (200 OK)
    client.force_authenticate(user=manager)
    response = client.post(f'/api/reviews/{review.id}/transition/', {'status': 'Approved', 'notes': 'Batch certified'})
    assert response.status_code == 200
    review.refresh_from_db()
    assert review.status == QualityReview.STATUS_APPROVED
    assert review.reviewed_by_manager == manager

    # 4. Verify supplier overall score was updated
    supplier.refresh_from_db()
    assert supplier.overall_quality_score == Decimal('95.00')
