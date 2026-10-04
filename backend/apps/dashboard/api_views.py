from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from apps.suppliers.models import Supplier
from apps.reviews.models import QualityReview


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_suppliers = Supplier.objects.count()
        active_suppliers = Supplier.objects.filter(status=Supplier.STATUS_ACTIVE).count()
        pending_reviews = QualityReview.objects.filter(
            status__in=[QualityReview.STATUS_PENDING_REVIEW, QualityReview.STATUS_UNDER_REVIEW]
        ).count()
        approved_reviews = QualityReview.objects.filter(status=QualityReview.STATUS_APPROVED).count()
        rejected_reviews = QualityReview.objects.filter(status=QualityReview.STATUS_REJECTED).count()

        avg_score_data = Supplier.objects.filter(
            status=Supplier.STATUS_ACTIVE,
            overall_quality_score__gt=0
        ).aggregate(Avg('overall_quality_score'))
        avg_score = round(avg_score_data['overall_quality_score__avg'] or 0.0, 1)

        # Status distribution for Doughnut Chart
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

        # Category average quality scores
        cat_scores = (
            Supplier.objects.values('category')
            .annotate(avg=Avg('overall_quality_score'))
            .order_by('category')
        )
        category_scores = {
            c['category']: round(float(c['avg'] or 0.0), 1) for c in cat_scores
        }

        # Top 5 and Bottom 5 Suppliers
        top_suppliers = list(
            Supplier.objects.filter(overall_quality_score__gt=0)
            .order_by('-overall_quality_score')[:5]
            .values('name', 'code', 'category', 'overall_quality_score', 'status')
        )

        bottom_suppliers = list(
            Supplier.objects.filter(overall_quality_score__gt=0)
            .order_by('overall_quality_score')[:5]
            .values('name', 'code', 'category', 'overall_quality_score', 'status')
        )

        # Recent 5 reviews
        recent_reviews = list(
            QualityReview.objects.select_related('supplier', 'reviewer')
            .order_by('-created_at')[:5]
            .values(
                'review_id', 'supplier__name', 'reviewer__username',
                'overall_score', 'status', 'created_at'
            )
        )

        return Response({
            'kpis': {
                'total_suppliers': total_suppliers,
                'active_suppliers': active_suppliers,
                'pending_reviews': pending_reviews,
                'approved_reviews': approved_reviews,
                'rejected_reviews': rejected_reviews,
                'average_quality_score': avg_score,
            },
            'charts': {
                'status_distribution': status_distribution,
                'category_scores': category_scores,
                'top_suppliers': top_suppliers,
                'bottom_suppliers': bottom_suppliers,
            },
            'recent_reviews': recent_reviews,
        })
