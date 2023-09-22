from django.urls import path, include
from . import views

app_name = 'book'
urlpatterns = [
    path('', views.home, name="home"),
    path('book/<int:pk>/<slug:slug>/', views.BookDetailView.as_view(), name="book_detail"),
    path('books/', views.BookListView.as_view(), name="book_list")
]