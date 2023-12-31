# Generated by Django 4.2.5 on 2023-09-24 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_alter_book_category_alter_bookcomment_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_categories', to='book.category'),
        ),
        migrations.AlterField(
            model_name='bookcomment',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='book_comments', to='book.book'),
        ),
    ]
