import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from requests.models import WorkloadRequest
from departments.models import Department
from subjects.models import Subject
from teachers.models import Teacher

# Get departments
dept_at = Department.objects.filter(code='AT').first()
dept_mf = Department.objects.filter(code='MF').first()

if dept_at and dept_mf:
    subject = Subject.objects.first()
    teacher = Teacher.objects.first()

    if subject:
        req, created = WorkloadRequest.objects.get_or_create(
            from_department=dept_at,
            to_department=dept_mf,
            subject=subject,
            semester=1,
            defaults={
                'total_hours': 60,
                'lecture_hours': 30,
                'practical_hours': 30,
                'message': "Iltimos, ushbu fanni o'qitishga ruxsat bering",
                'status': 'pending'
            }
        )
        print(f"{'✅ Создана' if created else 'ℹ️ Существует'} заявка #{req.id}")
    else:
        print("❌ Fan topilmadi!")
else:
    print("❌ Kafedralar topilmadi!")

print("\n🎉 Talabnoma tayyor!")