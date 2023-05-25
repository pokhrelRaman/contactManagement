# Generated by Django 4.2.1 on 2023-05-25 16:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contactManagement', '0003_contacts_blacklist'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
