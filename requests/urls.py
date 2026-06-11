from django.urls import path
from . import views

urlpatterns = [
    path('', views.request_list, name='request_list'),
    path('create/', views.request_create, name='request_create'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('<int:pk>/approve/', views.request_approve, name='request_approve'),
    path('<int:pk>/reject/', views.request_reject, name='request_reject'),
    path('<int:pk>/cancel/', views.request_cancel, name='request_cancel'),
    path('<int:pk>/delete/', views.request_delete, name='request_delete'),
]