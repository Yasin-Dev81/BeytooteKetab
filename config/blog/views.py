from django.shortcuts import render
from django.views import generic

from .models import Blog


class BlogListView(generic.ListView):
    template_name = 'blog/blog_list.html'
    model = Blog
