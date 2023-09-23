from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Blog, BlogCategory
from .forms import BlogCommentForm
from book.models import Book


class BlogListView(generic.ListView):
    template_name = 'blog/blog_list.html'
    model = Blog


class BlogDetailView(View):
    model = Blog
    template_name = 'blog/blog_detail.html'
    from_class = BlogCommentForm

    def setup(self, request, *args, **kwargs):
        self.blog = get_object_or_404(self.model, pk=kwargs.get('pk'))
        self.comments = self.blog.blog_comments.filter(is_pub=True)
        self.category = BlogCategory.objects.get(pk=self.blog.category.pk).blog_categories.all()[:3]
        self.book = Book.objects.all().order_by('-datetime_created')[:3]
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.blog.slug == kwargs['slug']:
            return redirect(reverse('blog:blog_detail', args=(self.kwargs['pk'], self.blog.slug, )))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.from_class
        return render(
            request,
            self.template_name,
            {"blog": self.blog, "comments": self.comments, "form": form, "category": self.category, "book": self.book}
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)
        if form.is_valid():
            form.save(commit=True, blog=self.blog, user=request.user)
            messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
            return redirect(reverse('blog:blog_detail', args=(self.kwargs['pk'], self.kwargs['slug'], )))
        return render(
            request,
            self.template_name,
            {'blog': self.book, 'comments': self.comments, 'form': form, "category": self.category, "book": self.book}
        )
