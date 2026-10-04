from rest_framework.routers import DefaultRouter
from .api_views import QualityReviewViewSet

router = DefaultRouter()
router.register(r'', QualityReviewViewSet, basename='qualityreview')

urlpatterns = router.urls
