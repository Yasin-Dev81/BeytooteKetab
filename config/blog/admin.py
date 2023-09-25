from django.contrib import admin
from .models import BlogCategory, Blog, BlogComment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]

    prepopulated_fields = {
        'slug': ['name', ]
    }


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'datetime_created',
    ]
    search_fields = [
        'title'
    ]
    list_filter = ['datetime_created']
    ordering = ['datetime_created']

    prepopulated_fields = {
        'slug': ['title', ]
    }
    raw_id_fields = [
        'category'
    ]


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = [
        'blog',
        'author',
        'is_pub',
        'datetime_created'
    ]
    search_fields = [
        'blog'
    ]
    list_filter = ['datetime_created']
    ordering = ['datetime_created']

    raw_id_fields = [
        'blog',
        'author',
    ]