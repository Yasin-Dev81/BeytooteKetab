from django.contrib import admin
from .models import Category, Book, Lang, BookComment, BookFile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
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
        'like_count'
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


@admin.register(Lang)
class LangAdmin(admin.ModelAdmin):
    list_display = ['lang']


@admin.register(BookComment)
class BookCommentAdmin(admin.ModelAdmin):
    list_display = [
        'book',
        'author',
        'is_pub',
        'datetime_created'
    ]
    search_fields = [
        'book'
    ]
    list_filter = ['datetime_created']
    ordering = ['datetime_created']

    raw_id_fields = [
        'book',
        'author',
    ]


@admin.register(BookFile)
class BookFileAdmin(admin.ModelAdmin):
    list_display = [
        '__str__'
    ]
    search_fields = [
        'book'
    ]
    list_filter = ['book']
    ordering = ['book']

    raw_id_fields = [
        'book',
    ]
