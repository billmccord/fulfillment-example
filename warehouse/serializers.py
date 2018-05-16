from rest_framework import serializers

from warehouse.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="warehouse:order-detail",
    )

    class Meta:
        model = Order
        fields = (
            'url',
            'id',
            'company',
            'address',
            'status',
            'deliver_by',
            'created_at',
            'updated_at',
        )