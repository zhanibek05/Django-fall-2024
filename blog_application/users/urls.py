from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile_edit, name='profile'),
    path('users/<int:id>', views.user_profile, name="profile")
]
