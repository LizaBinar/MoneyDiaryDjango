from django.urls import path

from .views import *

urlpatterns = [path('user_profile/<int:pk>/', ShowProfilePageView.as_view(), name='user_profile'),
               path('create_profile_page/', CreateProfilePageView.as_view(), name='create_user_profile'),
               path('update_profile_page/<int:pk>/', ProfileUpdateView.as_view(), name='update_user_profile')
               ]
