from django.urls import path
from .views import UserRegisterView, ProfileView, PasswordResetRequestView, PasswordResetView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),
    path('password/reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/', PasswordResetView.as_view(), name='password-reset'),
]