from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('home:category_filter', args=[self.slug, ])


class Book(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()
    main_lang = models.CharField(default='en', max_length=3)
    writer = models.CharField(max_length=200)
    image = models.ImageField()

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    premium_required = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book:book_detail', args=[self.pk, self.slug, ])
