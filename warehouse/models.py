import uuid

from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        blank=False,
        null=False,
        auto_now=True,
    )

    class Meta:
        abstract = True


class Order(BaseModel):
    company = models.CharField(
        blank=False,
        null=False,
        max_length=255,
    )
    address = models.CharField(
        blank=False,
        null=False,
        max_length=255,
    )
    status = models.CharField(
        max_length=50,
    )
    deliver_by = models.DateTimeField(
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    class Meta:
        app_label = 'warehouse'
