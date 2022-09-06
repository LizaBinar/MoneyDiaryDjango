from django.contrib.auth import views
from django.urls import path

urlpatterns = [
    # Вход
    path('login/', views.LoginView.as_view(), name='login'),
    # Выход
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Сброс пароля
    path('password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Смена пароля
    path('password-change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done')
]
