from django.urls import path, include
from . import views

app_name = 'order'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name="user_profile"),
    path('premiums/', views.PremiumPlansView.as_view(), name="premium_plans"),
    path('create/<int:plan_id>/', views.OrderCreateView.as_view(), name="create_order"),
    path('pay/<int:order_id>/', views.ZPOrderPayView.as_view(), name="pay_order"),
    path('verify/', views.OrderVerifyView.as_view(), name="verify_order")
]
