import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from subjects.models import Subject
from departments.models import Department

# Получаем кафедры
dept_at = Department.objects.get(code='AT')
dept_mf = Department.objects.get(code='MF')
dept_fal = Department.objects.get(code='FAL')
dept_st = Department.objects.get(code='ST')

subjects_data = [
    {"name": "Python Dasturlash", "code": "PY101", "department": dept_at, "subject_type": "core", "semester": 1, "credits": 5, "total_hours": 150, "lecture_hours": 30, "practical_hours": 60, "lab_hours": 60, "exam_type": "exam"},
    {"name": "Web Dasturlash", "code": "WEB102", "department": dept_at, "subject_type": "core", "semester": 2, "credits": 5, "total_hours": 150, "lecture_hours": 30, "practical_hours": 60, "lab_hours": 60, "exam_type": "project"},
    {"name": "Oliy Matematika", "code": "MATH101", "department": dept_mf, "subject_type": "core", "semester": 1, "credits": 4, "total_hours": 120, "lecture_hours": 40, "practical_hours": 80, "lab_hours": 0, "exam_type": "exam"},
    {"name": "Falsafa", "code": "PHIL101", "department": dept_fal, "subject_type": "general", "semester": 2, "credits": 3, "total_hours": 90, "lecture_hours": 30, "practical_hours": 60, "lab_hours": 0, "exam_type": "test"},
    {"name": "Ingliz tili", "code": "ENG101", "department": dept_st, "subject_type": "general", "semester": 1, "credits": 3, "total_hours": 90, "lecture_hours": 20, "practical_hours": 70, "lab_hours": 0, "exam_type": "test"},
]

for subj in subjects_data:
    s, created = Subject.objects.get_or_create(
        code=subj["code"],
        defaults=subj
    )
    print(f"{'✅ Создан' if created else 'ℹ️ Существует'} fan: {s.name}")

print("\n🎉 Все фаны добавлены!")