from django.urls import path
from . import views

urlpatterns = [
    path('', views.workload_list, name='workload_list'),
    path('create/', views.workload_create, name='workload_create'),
    path('<int:pk>/', views.workload_detail, name='workload_detail'),
    path('<int:pk>/edit/', views.workload_edit, name='workload_edit'),
    path('<int:pk>/delete/', views.workload_delete, name='workload_delete'),
    path('teacher/<int:teacher_id>/', views.workload_teacher_view, name='workload_teacher_view'),
    path('summary/', views.workload_summary, name='workload_summary'),
]