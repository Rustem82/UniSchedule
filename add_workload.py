import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from workload.models import Workload
from teachers.models import Teacher
from subjects.models import Subject
from groups.models import AcademicGroup

# Get first records
teacher = Teacher.objects.first()
subject = Subject.objects.first()
group = AcademicGroup.objects.first()

if teacher and subject and group:
    workload, created = Workload.objects.get_or_create(
        teacher=teacher,
        subject=subject,
        group=group,
        semester=1,
        academic_year='2024-2025',
        defaults={
            'lecture_hours': 30,
            'practical_hours': 30,
            'lab_hours': 20,
            'independent_hours': 40,
        }
    )
    print(f"{'✅ Создана' if created else 'ℹ️ Существует'} нагрузка: {workload}")
    print(f"   Jami soatlar: {workload.total_hours}")
else:
    print("❌ Ma'lumotlar topilmadi!")

print("\n🎉 Yuklama tayyor!")