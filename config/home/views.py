from django.shortcuts import render
from django.views import View

from book.models import Book
from blog.models import Blog


class HomeView(View):
    template_name = 'home/home.html'
    counte_each = 4

    def setup(self, request, *args, **kwargs):
        self.best_books = sorted(Book.objects.all(), key=lambda t: int(t.like_count)*(-1))[:self.counte_each]
        self.last_books = Book.objects.all().order_by('-datetime_created')[:self.counte_each*2]
        self.last_blogs = Blog.objects.all()[:2]
        self.blogs = Blog.objects.all().order_by('?')[:3]
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={
                'best_book': self.best_books,
                'last_book': self.last_books,
                'last_blogs': self.last_blogs,
                'blogs': self.blogs
            }
        )


def about_view(request):
    last_books = Book.objects.all().order_by('-datetime_created')[:10]
    return render(request, 'home/about.html', {'last_book': last_books})


def contacts_view(request):
    last_books = Book.objects.all().order_by('-datetime_created')[:10]
    return render(request, 'home/contacts.html', {'last_book': last_books})


def faq_view(request):
    last_books = Book.objects.all().order_by('-datetime_created')[:10]
    return render(request, 'home/faq.html', {'last_book': last_books})


def privacy_view(request):
    last_books = Book.objects.all().order_by('-datetime_created')[:10]
    return render(request, 'home/privacy.html', {'last_book': last_books})
