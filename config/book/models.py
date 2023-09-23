from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book:home')


class Book(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='book_categories')

    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()

    langs = models.ManyToManyField('Lang', related_name='book_langs')

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

    @property
    def like_count(self):
        return self.favorites.count()


class Lang(models.Model):
    lang = models.CharField(max_length=200)

    def __str__(self):
        return self.lang


class BookComment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments', blank=True, null=True)
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)

    is_pub = models.BooleanField(default=True)

    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_comments', null=True, blank=True)
    is_sub = models.BooleanField(default=False)

    class Meta:
        ordering = ('datetime_created',)

    def __str__(self):
        return "comment of %s" % self.author.phone_number

    def get_absolute_url(self):
        return reverse('book:book_detail', args=[self.book.pk, self.book.slug])
