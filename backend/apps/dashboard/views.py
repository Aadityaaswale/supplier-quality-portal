from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from apps.suppliers.models import Supplier
from apps.reviews.models import QualityReview
import json


@login_required
def dashboard_view(request):
    total_suppliers = Supplier.objects.count()
    active_suppliers = Supplier.objects.filter(status=Supplier.STATUS_ACTIVE).count()
    pending_reviews_count = QualityReview.objects.filter(
        status__in=[QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW]
    ).count()
    approved_reviews_count = QualityReview.objects.filter(status=QualityReview.STATUS_APPROVED).count()
    rejected_reviews_count = QualityReview.objects.filter(status=QualityReview.STATUS_REJECTED).count()

    avg_data = Supplier.objects.filter(
        status=Supplier.STATUS_ACTIVE,
        overall_quality_score__gt=0
    ).aggregate(Avg('overall_quality_score'))
    avg_quality_score = round(avg_data['overall_quality_score__avg'] or 0.0, 1)

    # Status distribution for Doughnut chart
    status_counts = dict(
        QualityReview.objects.values_list('status').annotate(count=Count('id'))
    )
    status_distribution = {
        'Draft': status_counts.get(QualityReview.STATUS_DRAFT, 0),
        'Pending Review': status_counts.get(QualityReview.STATUS_PENDING_REVIEW, 0),
        'Under Review': status_counts.get(QualityReview.STATUS_UNDER_REVIEW, 0),
        'Approved': status_counts.get(QualityReview.STATUS_APPROVED, 0),
        'Rejected': status_counts.get(QualityReview.STATUS_REJECTED, 0),
    }

    # Category performance
    cat_scores = (
        Supplier.objects.values('category')
        .annotate(avg=Avg('overall_quality_score'))
        .order_by('category')
    )
    category_labels = [c['category'] for c in cat_scores]
    category_data = [round(float(c['avg'] or 0.0), 1) for c in cat_scores]

    # Top 5 and Bottom 5 Suppliers
    top_suppliers = (
        Supplier.objects.filter(overall_quality_score__gt=0)
        .order_by('-overall_quality_score')[:5]
    )
    bottom_suppliers = (
        Supplier.objects.filter(overall_quality_score__gt=0)
        .order_by('overall_quality_score')[:5]
    )

    # Pending approvals for Quality Managers & Admins
    pending_approvals = QualityReview.objects.filter(
        status__in=[QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW]
    ).select_related('supplier', 'reviewer').order_by('-created_at')[:5]

    # Recent reviews
    recent_reviews = QualityReview.objects.select_related(
        'supplier', 'reviewer'
    ).order_by('-created_at')[:6]

    context = {
        'total_suppliers': total_suppliers,
        'active_suppliers': active_suppliers,
        'pending_reviews_count': pending_reviews_count,
        'approved_reviews_count': approved_reviews_count,
        'rejected_reviews_count': rejected_reviews_count,
        'avg_quality_score': avg_quality_score,
        'status_distribution_json': json.dumps(status_distribution),
        'category_labels_json': json.dumps(category_labels),
        'category_data_json': json.dumps(category_data),
        'top_suppliers': top_suppliers,
        'bottom_suppliers': bottom_suppliers,
        'pending_approvals': pending_approvals,
        'recent_reviews': recent_reviews,
    }

    return render(request, 'dashboard/index.html', context)
