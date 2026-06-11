import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from faculties.models import Faculty
from departments.models import Department
from specializations.models import Specialization
from django.contrib.auth.models import User
from teachers.models import Teacher

print("📊 Заполнение базы данных тестовыми данными...")

# Создание факультетов
faculties_data = [
    {"name": "Amaliy fanlar fakulteti", "code": "AF", "description": "Amaliy fanlar fakulteti"},
    {"name": "Sharq sivilizatsiyasi va falsafa fakulteti", "code": "SHF", "description": "Sharq sivilizatsiyasi va falsafa fakulteti"},
    {"name": "Sharq xalqlari tillari va adabiyoti instituti", "code": "SHXTAI", "description": "Sharq xalqlari tillari va adabiyoti instituti"},
    {"name": "Tashqi siyosat va xalqaro iqtisodiy munosabatlar instituti", "code": "TSXIM", "description": "Tashqi siyosat va xalqaro iqtisodiy munosabatlar instituti"},
]

for faculty_data in faculties_data:
    faculty, created = Faculty.objects.get_or_create(
        code=faculty_data["code"],
        defaults=faculty_data
    )
    print(f"{'✅ Создан' if created else 'ℹ️ Существует'} факультет: {faculty.name}")

# Создание кафедр
departments_data = [
    {"name": "Axborot texnologiyalari kafedrasi", "code": "AT", "faculty_code": "AF"},
    {"name": "Matematik fanlar kafedrasi", "code": "MF", "faculty_code": "AF"},
    {"name": "Falsafa kafedrasi", "code": "FAL", "faculty_code": "SHF"},
    {"name": "Siyosatshunoslik kafedrasi", "code": "SIY", "faculty_code": "SHF"},
    {"name": "Sharq tillari kafedrasi", "code": "ST", "faculty_code": "SHXTAI"},
    {"name": "Sharq adabiyoti kafedrasi", "code": "SA", "faculty_code": "SHXTAI"},
    {"name": "Xalqaro munosabatlar kafedrasi", "code": "XM", "faculty_code": "TSXIM"},
    {"name": "Iqtisodiyot kafedrasi", "code": "IQT", "faculty_code": "TSXIM"},
]

for dept_data in departments_data:
    try:
        faculty = Faculty.objects.get(code=dept_data["faculty_code"])
        department, created = Department.objects.get_or_create(
            code=dept_data["code"],
            defaults={
                "name": dept_data["name"],
                "faculty": faculty,
                "head_name": f"{dept_data['name']} mudiri",
            }
        )
        print(f"{'✅ Создана' if created else 'ℹ️ Существует'} кафедра: {department.name}")
    except Faculty.DoesNotExist:
        print(f"❌ Факультет {dept_data['faculty_code']} не найден для кафедры {dept_data['name']}")

# Создание специальностей
specializations_data = [
    {"name": "Kompyuter injiniringi", "code": "KI", "faculty_code": "AF", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Dasturiy injiniring", "code": "DI", "faculty_code": "AF", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Falsafa", "code": "FAL", "faculty_code": "SHF", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Sharq filologiyasi", "code": "SF", "faculty_code": "SHXTAI", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Xalqaro iqtisodiyot", "code": "XI", "faculty_code": "TSXIM", "education_type": "kunduzgi", "duration": 48, "credits": 240},
]

for spec_data in specializations_data:
    try:
        faculty = Faculty.objects.get(code=spec_data["faculty_code"])
        specialization, created = Specialization.objects.get_or_create(
            code=spec_data["code"],
            defaults={
                "name": spec_data["name"],
                "faculty": faculty,
                "education_type": spec_data["education_type"],
                "duration": spec_data["duration"],
                "credits": spec_data["credits"],
            }
        )
        print(f"{'✅ Создана' if created else 'ℹ️ Существует'} специальность: {specialization.name}")
    except Faculty.DoesNotExist:
        print(f"❌ Факультет {spec_data['faculty_code']} не найден для специальности {spec_data['name']}")

# Создание преподавателей
for i in range(1, 6):
    username = f'teacher{i}'
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username,
            password='teacher123',
            first_name=f'Teacher',
            last_name=f'{i}'
        )
        department = Department.objects.first()
        if department:
            teacher = Teacher.objects.create(
                user=user,
                department=department,
                position='teacher',
                employee_id=f'TCH00{i}',
                is_active=True
            )
            print(f"✅ Создан преподаватель: {teacher.user.get_full_name()}")
        else:
            print(f"❌ Нет кафедры для преподавателя {username}")
    else:
        print(f"ℹ️ Преподаватель {username} уже существует")

print("\n🎉 База данных успешно заполнена тестовыми данными!")
print("\nЛогины для входа:")
print("  Admin: admin / admin123")
print("  Teacher: teacher1 / teacher123")