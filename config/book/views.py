from django.shortcuts import render, redirect
from django.views import generic, View
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Book, Category, BookComment
from .forms import BookCommentForm


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
    from_class = BookCommentForm

    def setup(self, request, *args, **kwargs):
        self.book = get_object_or_404(self.model, pk=kwargs['pk'])
        self.comments = self.book.book_comments.filter(is_pub=True)
        self.category = Category.objects.get(pk=self.book.category.pk).book_categories.order_by('?')[:4]
        self.is_fav = False
        if request.user.is_authenticated:
            self.is_fav = self.book.favorites.filter(pk=request.user.pk).exists()
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.book.slug == kwargs['slug']:
            return redirect(reverse('book:book_detail', args=(self.kwargs['pk'], self.kwargs['slug'], )))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.from_class
        return render(
            request,
            self.template_name,
            {'book': self.book, 'comments': self.comments, 'form': form, 'is_fav': self.is_fav, 'category': self.category}
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.from_class(request.POST)
        if form.is_valid():
            form.save(commit=True, book=self.book, user=request.user)
            messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
            return redirect(reverse('book:book_detail', args=(self.kwargs['pk'], self.kwargs['slug'], )))
        return render(
            request,
            self.template_name,
            {'book': self.book, 'comments': self.comments, 'form': form, 'is_fav': self.is_fav, 'category': self.category}
        )


class BookListView(generic.ListView):
    model = Book
    template_name = 'book/catalog.html'
    paginate_by = 8

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()
        return context
