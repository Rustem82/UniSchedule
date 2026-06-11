from django.urls import path
from . import views

urlpatterns = [
    # Building URLs
    path('buildings/', views.building_list, name='building_list'),
    path('buildings/create/', views.building_create, name='building_create'),
    path('buildings/<int:pk>/', views.building_detail, name='building_detail'),
    path('buildings/<int:pk>/edit/', views.building_edit, name='building_edit'),
    path('buildings/<int:pk>/delete/', views.building_delete, name='building_delete'),

    # Room URLs
    path('', views.room_list, name='room_list'),
    path('create/', views.room_create, name='room_create'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    path('<int:pk>/edit/', views.room_edit, name='room_edit'),
    path('<int:pk>/delete/', views.room_delete, name='room_delete'),
]