# Generated by Django 4.2.5 on 2023-09-24 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_categories', to='blog.blogcategory'),
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='sub_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_blogcomments', to='blog.blogcomment'),
        ),
    ]
