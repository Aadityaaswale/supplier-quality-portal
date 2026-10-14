from rest_framework.routers import DefaultRouter
from .api_views import SupplierViewSet

router = DefaultRouter()
router.register(r'', SupplierViewSet, basename='api-supplier')

urlpatterns = router.urls
