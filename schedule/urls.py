from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule_list, name='schedule_list'),
    path('create/', views.schedule_create, name='schedule_create'),
    path('<int:pk>/', views.schedule_detail, name='schedule_detail'),
    path('<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
    path('group/<int:group_id>/', views.schedule_group_view, name='schedule_group_view'),
    path('teacher/<int:teacher_id>/', views.schedule_teacher_view, name='schedule_teacher_view'),
]