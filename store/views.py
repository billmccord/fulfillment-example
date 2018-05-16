from rest_framework import viewsets

from store.models import Order
from store.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
