# Generated by Django 4.2 on 2023-11-28 12:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stockmgmt', '0004_alter_stock_category_delete_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='time_stamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]