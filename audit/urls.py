from django.urls import path
from django.shortcuts import render

def audit_log(request):
    return render(request, 'audit/list.html', {'message': 'Audit logi bo\'limi ishlab chiqilmoqda'})

urlpatterns = [
    path('', audit_log, name='audit_log'),
]