from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('faculties/', include('faculties.urls')),
    path('departments/', include('departments.urls')),
    path('specializations/', include('specializations.urls')),
    path('teachers/', include('teachers.urls')),
    path('subjects/', include('subjects.urls')),
    path('groups/', include('groups.urls')),
    path('rooms/', include('rooms.urls')),
    path('schedule/', include('schedule.urls')),
    path('workload/', include('workload.urls')),
    path('requests/', include('requests.urls')),
    path('audit/', include('audit.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
]