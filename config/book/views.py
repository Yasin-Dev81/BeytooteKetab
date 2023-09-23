from django.shortcuts import render, redirect
from django.views import generic, View
from .models import Book, Category, BookComment
from django.shortcuts import get_object_or_404
from django.urls import reverse


class HomeView(View):
    template_name = 'book/home.html'
    counte_each = 4

    def setup(self, request, *args, **kwargs):
        self.best_books = sorted(Book.objects.all(), key=lambda t: int(t.like_count)*(-1))[:self.counte_each]
        self.last_books = Book.objects.all().order_by('-datetime_created')[:self.counte_each*2]
        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={
                'best_book': self.best_books,
                'last_book': self.last_books
            }
        )


class BookDetailView(View):
    model = Book
    template_name = 'book/detail.html'

    def setup(self, request, *args, **kwargs):
        self.comments = BookComment.objects.filter(pk=kwargs['pk'])
        self.book = get_object_or_404(self.model, pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.book.slug == kwargs['slug']:
            return redirect(reverse('book:book_detail', args=(self.book.pk, self.book.slug, )))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'book': self.book, 'comments': self.comments})


class BookListView(generic.ListView):
    model = Book
    template_name = 'book/catalog.html'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()
        return context
