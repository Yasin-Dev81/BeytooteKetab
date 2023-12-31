# Generated by Django 4.2.5 on 2023-09-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_alter_book_writer'),
        ('accounts', '0003_user_favorites_delete_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='book.book'),
        ),
    ]
