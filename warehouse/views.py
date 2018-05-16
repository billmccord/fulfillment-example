from rest_framework import viewsets, status

from warehouse.models import Order
from warehouse.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
