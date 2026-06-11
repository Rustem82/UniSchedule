import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from groups.models import AcademicGroup
from specializations.models import Specialization

# Получаем специальности
ki = Specialization.objects.get(code='KI')
di = Specialization.objects.get(code='DI')
fal = Specialization.objects.get(code='FAL')

groups_data = [
    {"name": "KI-101", "specialization": ki, "year_of_admission": 2024, "current_course": 1, "student_count": 25, "language": "uzbek"},
    {"name": "KI-102", "specialization": ki, "year_of_admission": 2024, "current_course": 1, "student_count": 24, "language": "uzbek"},
    {"name": "DI-101", "specialization": di, "year_of_admission": 2024, "current_course": 1, "student_count": 22, "language": "english"},
    {"name": "FAL-101", "specialization": fal, "year_of_admission": 2024, "current_course": 1, "student_count": 20, "language": "uzbek"},
]

for grp in groups_data:
    g, created = AcademicGroup.objects.get_or_create(
        name=grp["name"],
        year_of_admission=grp["year_of_admission"],
        defaults=grp
    )
    print(f"{'✅ Создана' if created else 'ℹ️ Существует'} группа: {g.name}")

print("\n🎉 Все группы добавлены!")