from django.urls import path
from .views import *

urlpatterns = [
    path('', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/edit/', user_profile_edit, name='user_profile_edit'),
]
