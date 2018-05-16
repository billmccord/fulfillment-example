from rest_framework import serializers

from store.models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="store:order-detail",
    )

    class Meta:
        model = Order
        fields = (
            'url',
            'id',
            'company',
            'address',
            'total',
            'currency',
            'status',
            'deliver_by',
            'created_at',
            'updated_at',
        )
