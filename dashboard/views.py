from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from faculties.models import Faculty
from departments.models import Department
from teachers.models import Teacher
from specializations.models import Specialization


@login_required
def dashboard_view(request):
    # Основная статистика
    total_faculties = Faculty.objects.count()
    total_departments = Department.objects.count()
    total_teachers = Teacher.objects.filter(is_active=True).count()
    total_specializations = Specialization.objects.count()

    # Статистика по факультетам
    faculties_data = []
    for faculty in Faculty.objects.all():
        faculties_data.append({
            'name': faculty.name,
            'code': faculty.code,
            'department_count': faculty.departments.count(),
            'teacher_count': sum([dept.teachers.count() for dept in faculty.departments.all()]),
            'specialization_count': faculty.specializations.count(),
        })

    # Свежие данные
    recent_faculties = Faculty.objects.all().order_by('-created_at')[:5]
    recent_departments = Department.objects.all().select_related('faculty').order_by('-created_at')[:5]
    recent_teachers = Teacher.objects.select_related('user', 'department').all().order_by('-created_at')[:5]

    # График: факультеты по кафедрам
    chart_labels = [f.name for f in Faculty.objects.all()]
    chart_data = [f.departments.count() for f in Faculty.objects.all()]

    context = {
        'total_faculties': total_faculties,
        'total_departments': total_departments,
        'total_teachers': total_teachers,
        'total_specializations': total_specializations,
        'faculties_data': faculties_data,
        'recent_faculties': recent_faculties,
        'recent_departments': recent_departments,
        'recent_teachers': recent_teachers,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'dashboard/dashboard.html', context)