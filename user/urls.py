from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('otp/verify/', views.OtpVerifyView.as_view(), name='login'),
    path('password_reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.PasswordResetValidateTokenView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('user/', views.UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
