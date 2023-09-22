from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('forgot/', views.UserPasswordResetView.as_view(), name='forgot_password'),
    path('forgot/verify/', views.UserPasswordResetVerifyCodeView.as_view(), name='forgot_password_verify'),
]
