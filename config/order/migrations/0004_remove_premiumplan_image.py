# Generated by Django 4.2.5 on 2023-09-24 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_premiumplan_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='premiumplan',
            name='image',
        ),
    ]