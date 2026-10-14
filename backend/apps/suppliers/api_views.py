from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from .models import Supplier
from .serializers import SupplierSerializer
from apps.accounts.permissions import IsQualityManagerOrAdmin, IsReviewerOrHigher


class SupplierPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = SupplierPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'supplier_id', 'contact_person', 'category']
    ordering_fields = ['name', 'created_at', 'overall_quality_score']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsQualityManagerOrAdmin()]
        return [IsReviewerOrHigher()]
