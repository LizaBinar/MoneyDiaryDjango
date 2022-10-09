from django.urls import path

from . import views

urlpatterns = [path('user_profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='user_profile'),
               path('create_profile_page/', views.CreateProfilePageView.as_view(), name='create_user_profile'),
               path('update_profile_page/<int:pk>/', views.ProfileUpdateView.as_view(), name='update_user_profile')
               ]
