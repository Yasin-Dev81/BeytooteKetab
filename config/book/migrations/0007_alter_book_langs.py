# Generated by Django 4.2.5 on 2023-09-23 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_remove_book_main_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='langs',
            field=models.ManyToManyField(related_name='book_langs', to='book.lang'),
        ),
    ]
