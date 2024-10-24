from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('query-builder/', views.query_builder, name='query_builder'),
    path('users/', views.UserListView.as_view(), name='user_list'),  # List users
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),  # Create user
    path('users/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),  # Update user
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),  # Delete user

    
    # path('filter_companies/', views.filter_companies, name='filter_companies'),
]
