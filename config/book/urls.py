from django.urls import path, include
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.BookListView.as_view(), name="book_list"),
    path('book/<int:pk>/<slug:slug>/', views.BookDetailView.as_view(), name="book_detail")
]
