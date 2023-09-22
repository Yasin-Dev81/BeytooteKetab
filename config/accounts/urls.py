from django.urls import path, include
from . import views

app_name = 'accounts'

favorites_url = [
    path('', views.UserFavoritesView.as_view(), name='user_favorites'),
    path('add/<int:pk>/', views.AddFavoritesView.as_view(), name='add_favorites'),
    path('remove/<int:pk>/', views.RemoveFavoritesView.as_view(), name='remove_favorites')
]

info_url = [
    path('edit/', views.EditUserInfoView.as_view(), name='user_info_edit')
]

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('forgot/', views.UserPasswordResetView.as_view(), name='forgot_password'),
    path('forgot/verify/', views.UserPasswordResetVerifyCodeView.as_view(), name='forgot_password_verify'),

    path('info/', include(info_url)),
    path('favorites/', include(favorites_url)),
]
