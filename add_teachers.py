import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from teachers.models import Teacher
from departments.models import Department
from django.contrib.auth.models import User

# Получаем кафедры
dept_at = Department.objects.get(code='AT')
dept_mf = Department.objects.get(code='MF')
dept_fal = Department.objects.get(code='FAL')
dept_st = Department.objects.get(code='ST')

teachers_data = [
    {"username": "karimov_a", "first_name": "Akmal", "last_name": "Karimov", "password": "teacher123", "department": dept_at, "position": "head", "academic_degree": "professor", "employee_id": "TCH001"},
    {"username": "rahimov_b", "first_name": "Bakhtiyor", "last_name": "Rahimov", "password": "teacher123", "department": dept_mf, "position": "professor", "academic_degree": "dsc", "employee_id": "TCH002"},
    {"username": "nazarov_c", "first_name": "Cahongir", "last_name": "Nazarov", "password": "teacher123", "department": dept_fal, "position": "docent", "academic_degree": "phd", "employee_id": "TCH003"},
    {"username": "tursunov_e", "first_name": "Elbek", "last_name": "Tursunov", "password": "teacher123", "department": dept_st, "position": "senior_teacher", "academic_degree": "none", "employee_id": "TCH004"},
]

for t_data in teachers_data:
    if not User.objects.filter(username=t_data["username"]).exists():
        user = User.objects.create_user(
            username=t_data["username"],
            password=t_data["password"],
            first_name=t_data["first_name"],
            last_name=t_data["last_name"]
        )
        teacher = Teacher.objects.create(
            user=user,
            department=t_data["department"],
            position=t_data["position"],
            academic_degree=t_data["academic_degree"],
            employee_id=t_data["employee_id"],
            is_active=True
        )
        print(f"✅ Создан преподаватель: {teacher.get_full_name()}")
    else:
        print(f"ℹ️ Преподаватель {t_data['username']} уже существует")

print("\n🎉 Все преподаватели добавлены!")