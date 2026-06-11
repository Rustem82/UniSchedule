import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from schedule.models import Schedule
from groups.models import AcademicGroup
from subjects.models import Subject
from teachers.models import Teacher
from rooms.models import Room

# Get first group, subject, teacher, room
group = AcademicGroup.objects.first()
subject = Subject.objects.first()
teacher = Teacher.objects.first()
room = Room.objects.first()

if group and subject and teacher and room:
    schedule, created = Schedule.objects.get_or_create(
        group=group,
        day_of_week=1,
        lesson_number=1,
        week_type='all',
        defaults={
            'subject': subject,
            'teacher': teacher,
            'room': room,
            'lesson_type': 'lecture',
            'subgroup': 1,
            'academic_year': '2024-2025',
            'semester': 1
        }
    )
    print(f"{'✅ Создан' if created else 'ℹ️ Существует'} dars: {schedule}")
else:
    print("❌ Ma'lumotlar topilmadi. Avval guruh, fan, o'qituvchi va xona qo'shing!")

print("\n🎉 Dars jadvali tayyor!")