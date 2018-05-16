import json
import logging

import requests
from django.contrib import admin
from django.forms import model_to_dict
from rest_framework.reverse import reverse as rest_reverse

from fulfillment.utils import CustomJsonEncoder
from store.models import Order


class OrderAdmin(admin.ModelAdmin):
    logger = logging.getLogger(__name__)

    # A handy constant for the name of the alternate database.
    using = 'store_db'

    def save_model(self, request, obj, form, change):
        is_update = obj.created_at is not None

        obj.save(using=self.using)

        # Save the object to the warehouse as well.
        headers = {'Content-Type': 'application/json'}
        data = model_to_dict(
            obj,
            fields=(
                'id',
                'company',
                'address',
                'status',
                'deliver_by',
            ),
        )

        if is_update:
            url = request.build_absolute_uri(rest_reverse(
                'warehouse:order-detail',
                args=[obj.id],
            ))
            resp = requests.patch(
                url,
                data=json.dumps(data, cls=CustomJsonEncoder),
                headers=headers,
            )
        else:
            url = request.build_absolute_uri(rest_reverse(
                'warehouse:order-list',
            ))
            resp = requests.post(
                url,
                data=json.dumps(data, cls=CustomJsonEncoder),
                headers=headers,
            )

        self.logger.debug(
            'Store order saved to warehouse status: {}; reason: {}'.format(
                resp.status_code,
                resp.reason,
            ),
        )

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super().formfield_for_foreignkey(
            db_field,
            request,
            using=self.using,
            **kwargs,
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super().formfield_for_manytomany(
            db_field,
            request,
            using=self.using,
            **kwargs,
        )


admin.site.register(Order, OrderAdmin)
