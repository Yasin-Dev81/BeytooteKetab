from django.urls import path, include
from . import views

app_name = 'order'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name="user_profile"),
    path('premiums/', views.PremiumPlansView.as_view(), name="premium_plans")
]
