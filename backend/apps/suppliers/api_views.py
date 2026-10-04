from rest_framework import viewsets, filters
from .models import Supplier
from .serializers import SupplierSerializer
from apps.accounts.permissions import IsQualityManagerOrAdmin, IsReviewerOrHigher


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'supplier_id', 'contact_person', 'category']
    ordering_fields = ['name', 'created_at', 'overall_quality_score']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsQualityManagerOrAdmin()]
        return [IsReviewerOrHigher()]
