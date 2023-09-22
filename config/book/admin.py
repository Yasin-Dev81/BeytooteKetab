from django.contrib import admin
from .models import Category, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
    ]

    prepopulated_fields = {
        'slug': ['name', ]
    }


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'category',
        'premium_required',
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

