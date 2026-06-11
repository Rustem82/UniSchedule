from django.urls import path
from . import views

urlpatterns = [
    path('', views.specialization_list, name='specialization_list'),
    path('create/', views.specialization_create, name='specialization_create'),
    path('<int:pk>/', views.specialization_detail, name='specialization_detail'),
    path('<int:pk>/edit/', views.specialization_edit, name='specialization_edit'),
    path('<int:pk>/delete/', views.specialization_delete, name='specialization_delete'),
]