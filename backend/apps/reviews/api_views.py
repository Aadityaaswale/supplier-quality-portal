from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import QualityReview, ReviewAuditLog
from .serializers import QualityReviewSerializer
from apps.accounts.permissions import IsReviewerOrHigher, IsQualityManagerOrAdmin


class QualityReviewViewSet(viewsets.ModelViewSet):
    queryset = QualityReview.objects.select_related('supplier', 'reviewer').all()
    serializer_class = QualityReviewSerializer
    permission_classes = [IsReviewerOrHigher]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['review_id', 'supplier__name', 'reviewer__username', 'status']
    ordering_fields = ['review_date', 'overall_score', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        review = serializer.save(reviewer=self.request.user)
        ReviewAuditLog.objects.create(
            review=review,
            actor=self.request.user,
            action=ReviewAuditLog.ACTION_CREATED,
            old_status='',
            new_status=review.status,
            notes='Initial review draft created.'
        )

    @action(detail=True, methods=['post'], url_path='transition')
    def transition_status(self, request, pk=None):
        review = self.get_object()
        target_status = request.data.get('status')
        notes = request.data.get('notes', '')
        user = request.user
        role = getattr(user.profile, 'role', 'REVIEWER') if hasattr(user, 'profile') else 'REVIEWER'
        if user.is_superuser:
            role = 'ADMIN'

        old_status = review.status

        # Transition 1: Submit review (Draft -> Pending Review)
        if target_status == QualityReview.STATUS_PENDING_REVIEW:
            if review.status != QualityReview.STATUS_DRAFT:
                return Response(
                    {'error': f"Cannot submit review in '{review.status}' state."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            review.status = QualityReview.STATUS_PENDING_REVIEW
            review.save()
            ReviewAuditLog.objects.create(
                review=review,
                actor=user,
                action=ReviewAuditLog.ACTION_SUBMITTED,
                old_status=old_status,
                new_status=review.status,
                notes=notes or 'Review submitted for Manager evaluation.'
            )
            return Response(self.get_serializer(review).data)

        # Transition 2: Move to Under Review
        elif target_status == QualityReview.STATUS_UNDER_REVIEW:
            if role not in ['ADMIN', 'QUALITY_MANAGER']:
                raise PermissionDenied("Only Quality Managers or Admins can review pending audits.")
            review.status = QualityReview.STATUS_UNDER_REVIEW
            review.save()
            ReviewAuditLog.objects.create(
                review=review,
                actor=user,
                action=ReviewAuditLog.ACTION_UNDER_REVIEW,
                old_status=old_status,
                new_status=review.status,
                notes=notes or 'Review under active evaluation.'
            )
            return Response(self.get_serializer(review).data)

        # Transition 3: Approve
        elif target_status == QualityReview.STATUS_APPROVED:
            if role not in ['ADMIN', 'QUALITY_MANAGER']:
                raise PermissionDenied("Only Quality Managers or Admins can approve reviews.")
            review.status = QualityReview.STATUS_APPROVED
            review.manager_remarks = notes or request.data.get('manager_remarks', 'Approved by Quality Manager.')
            review.reviewed_by_manager = user
            review.save()
            ReviewAuditLog.objects.create(
                review=review,
                actor=user,
                action=ReviewAuditLog.ACTION_APPROVED,
                old_status=old_status,
                new_status=review.status,
                notes=notes or 'Review officially approved.'
            )
            return Response(self.get_serializer(review).data)

        # Transition 4: Reject
        elif target_status == QualityReview.STATUS_REJECTED:
            if role not in ['ADMIN', 'QUALITY_MANAGER']:
                raise PermissionDenied("Only Quality Managers or Admins can reject reviews.")
            review.status = QualityReview.STATUS_REJECTED
            review.manager_remarks = notes or request.data.get('manager_remarks', 'Rejected due to quality discrepancies.')
            review.reviewed_by_manager = user
            review.save()
            ReviewAuditLog.objects.create(
                review=review,
                actor=user,
                action=ReviewAuditLog.ACTION_REJECTED,
                old_status=old_status,
                new_status=review.status,
                notes=notes or 'Review rejected.'
            )
            return Response(self.get_serializer(review).data)

        return Response(
            {'error': f"Invalid target status '{target_status}' requested."},
            status=status.HTTP_400_BAD_REQUEST
        )
