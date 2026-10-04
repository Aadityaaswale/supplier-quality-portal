from rest_framework import serializers
from .models import QualityReview, ReviewAuditLog
from apps.suppliers.serializers import SupplierSerializer


class ReviewAuditLogSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.username', read_only=True)

    class Meta:
        model = ReviewAuditLog
        fields = ['id', 'action', 'actor_name', 'old_status', 'new_status', 'notes', 'timestamp']


class QualityReviewSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewer.username', read_only=True)
    audit_logs = ReviewAuditLogSerializer(many=True, read_only=True)

    class Meta:
        model = QualityReview
        fields = [
            'id', 'review_id', 'supplier', 'supplier_name', 'reviewer', 'reviewer_name',
            'review_date', 'defect_count', 'compliance_score', 'delivery_score',
            'product_quality_score', 'overall_score', 'status', 'comments',
            'manager_remarks', 'audit_logs', 'created_at', 'updated_at'
        ]
        read_only_fields = ['overall_score', 'created_at', 'updated_at']
