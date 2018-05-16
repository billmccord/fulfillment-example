# Generated by Django 2.0.5 on 2018-05-16 07:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('company', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('total', models.DecimalField(decimal_places=2, max_digits=19)),
                ('currency', models.CharField(default='HKD', max_length=20)),
                ('status', models.CharField(max_length=50)),
                ('deliver_by', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
