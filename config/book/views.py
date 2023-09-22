from django.shortcuts import render, redirect
from django.views import generic
from .models import Book


def home(request):
    return render(request, 'book/home.html')


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book/detail.html'
    pk_url_kwarg = "pk"


class BookListView(generic.ListView):
    model = Book
    template_name = 'book/catalog.html'
    paginate_by = 8
