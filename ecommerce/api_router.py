from business.views.product_views import ProductViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf import settings

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("products", ProductViewSet, basename="products viewset")

app_name = "Ecommerce"
urlpatterns = router.urls
