from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('query-builder/', views.query_builder, name='query_builder'),
    # path('filter_companies/', views.filter_companies, name='filter_companies'),
]
