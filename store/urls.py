from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from store.views import OrderViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]