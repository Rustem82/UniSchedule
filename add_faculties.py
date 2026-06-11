import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from faculties.models import Faculty

faculties = [
    {"name": "Amaliy fanlar fakulteti", "code": "AF"},
    {"name": "Sharq sivilizatsiyasi va falsafa fakulteti", "code": "SHF"},
    {"name": "Sharq xalqlari tillari va adabiyoti instituti", "code": "SHXTAI"},
    {"name": "Tashqi siyosat va xalqaro iqtisodiy munosabatlar instituti", "code": "TSXIM"},
]

for faculty_data in faculties:
    faculty, created = Faculty.objects.get_or_create(
        code=faculty_data["code"],
        defaults={"name": faculty_data["name"]}
    )
    if created:
        print(f"✅ Добавлен факультет: {faculty.name}")
    else:
        print(f"ℹ️ Факультет уже существует: {faculty.name}")

print("\n🎉 Все факультеты добавлены!")