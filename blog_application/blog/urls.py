from django.urls import path
from . import views

urlpatterns = [
    path('my_posts/', views.my_posts),
    path('my_posts/<int:id>', views.my_post),
    path('posts/', views.get_posts),
    path('posts/<int:id>', views.get_post),
    path('posts/create', views.create_post),

]
