from django.shortcuts import render, redirect
from django.views import generic, View
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .models import Book, Category, BookComment
from .forms import BookCommentForm


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
    context_object_name = 'books'
    paginate_by = 8

    def get_queryset(self):
        # Retrieve the selected sorting option from the GET parameters
        orderby = self.request.GET.get('sort', '-datetime_created')
        book_name = self.request.GET.get('book_name')

        # Retrieve the list of selected genres from the GET parameters
        selected_genres = [slug for slug in Category.objects.values_list('slug', flat=True) if self.request.GET.get(slug)]

        # Start with all books
        books = Book.objects.all()

        # Apply genre filters if selected
        if book_name:
            books = books.filter(title__contains=book_name)
        if selected_genres:
            books = books.filter(category__slug__in=selected_genres)

        # Apply sorting
        if "like_count" in orderby:
            books = sorted(books, key=lambda t: t.like_count * (-1))
        else:
            books = books.order_by(orderby)

        return books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the category list to the template
        context['category_list'] = Category.objects.all()

        # Pass the selected genres to the template
        context['selected_genres'] = [obj for obj in Category.objects.all() if self.request.GET.get(obj.slug)]

        return context
