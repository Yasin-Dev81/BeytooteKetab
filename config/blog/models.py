from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth import get_user_model


class BlogCategory(models.Model):
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


class Blog(models.Model):
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blog_categories')

    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()

    image = models.ImageField()
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-datetime_modified',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.pk, self.slug, ])


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comments')
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(auto_now_add=True)

    is_pub = models.BooleanField(default=True)

    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_blogcomments', null=True, blank=True)
    is_sub = models.BooleanField(default=False)

    class Meta:
        ordering = ('datetime_created',)

    def __str__(self):
        return "comment of %s" % self.author.phone_number

    def get_absolute_url(self):
        return reverse('blog:blog_detail', args=[self.blog.pk, self.blog.slug])
