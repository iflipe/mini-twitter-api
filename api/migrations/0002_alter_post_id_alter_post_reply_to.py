# Generated by Django 5.1.3 on 2024-12-13 23:57

import django.db.models.deletion
import shortuuid.django_fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, editable=False, length=22, max_length=22, prefix='', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='api.post'),
        ),
    ]