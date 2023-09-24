from django.urls import path

from . import views


app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about/', views.about_view, name="about"),
    path('contact/', views.contacts_view, name="contact"),
    path('faq/', views.faq_view, name="faq"),
    path('privacy/', views.privacy_view, name="privacy"),
]
