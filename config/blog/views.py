from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic, View
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Blog, BlogCategory
from .forms import BlogCommentForm, EmailForm
from book.models import Book


class BlogListView(generic.ListView):
    template_name = 'blog/blog_list.html'
    model = Blog


class BlogDetailView(View):
    model = Blog
    template_name = 'blog/blog_detail.html'
    comment_form_class = BlogCommentForm
    email_form_class = EmailForm

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
        email_form = self.email_form_class
        if request.user.is_authenticated:
            email_form = email_form(data={"email": request.user.email})
        return render(
            request,
            self.template_name,
            {
                "blog": self.blog, "comments": self.comments, "comment_form": self.comment_form_class,
                "category": self.category, "book": self.book, "email_form": email_form
            }
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        comment_form = self.comment_form_class(request.POST)
        email_form = self.email_form_class(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=True, blog=self.blog, user=request.user)
            messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
            return redirect(reverse('blog:blog_detail', args=(self.kwargs['pk'], self.kwargs['slug'], )))
        if email_form.is_valid():
            email_form.save(commit=True, user=request.user)
            messages.success(request, 'ایمیل شما با موفقیت ثبت شد', 'success')
            return redirect(reverse('blog:blog_detail', args=(self.kwargs['pk'], self.kwargs['slug'],)))
        return render(
            request,
            self.template_name,
            {
                "blog": self.blog, "comments": self.comments, "comment_form": comment_form,
                "category": self.category, "book": self.book, "email_form": email_form
            }
        )
