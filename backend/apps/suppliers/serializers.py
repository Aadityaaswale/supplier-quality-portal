from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    grade = serializers.ReadOnlyField()

    class Meta:
        model = Supplier
        fields = [
            'id', 'supplier_id', 'name', 'code', 'contact_person',
            'email', 'phone', 'address', 'category', 'status',
            'overall_quality_score', 'grade', 'created_at', 'updated_at'
        ]
        read_only_fields = ['overall_quality_score', 'grade', 'created_at', 'updated_at']
