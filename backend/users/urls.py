from django.urls import path
from .views import create_user, delete_user, user_detail, user_list, update_user   # Updated function names

urlpatterns = [
    path('users/', user_list, name="users_list"),
    path('users/create/', create_user, name="users_create"),  
    path('users/<str:id>/', user_detail, name="users_read"),
    path('users/<str:id>/delete/', delete_user, name="users_delete"),
    path('users/<str:id>/update/', update_user, name="users_update"),
    path('users/<str:id>/update/', update_user, name="users_update"), 
]
