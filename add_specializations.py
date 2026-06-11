import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from specializations.models import Specialization
from faculties.models import Faculty

# Получаем факультеты
af = Faculty.objects.get(code='AF')
shf = Faculty.objects.get(code='SHF')
shxtai = Faculty.objects.get(code='SHXTAI')
tsxim = Faculty.objects.get(code='TSXIM')

specializations = [
    {"name": "Kompyuter injiniringi", "code": "KI", "faculty": af, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Dasturiy injiniring", "code": "DI", "faculty": af, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Axborot xavfsizligi", "code": "AX", "faculty": af, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Falsafa", "code": "FAL", "faculty": shf, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Siyosatshunoslik", "code": "SIY", "faculty": shf, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Sharq filologiyasi", "code": "SF", "faculty": shxtai, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Xalqaro iqtisodiyot", "code": "XI", "faculty": tsxim, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
    {"name": "Xalqaro munosabatlar", "code": "XM", "faculty": tsxim, "degree_type": "bakalavr", "education_type": "kunduzgi", "duration": 48, "credits": 240},
]

for spec in specializations:
    s, created = Specialization.objects.get_or_create(
        code=spec["code"],
        defaults=spec
    )
    print(f"{'✅ Создана' if created else 'ℹ️ Существует'} специальность: {s.name}")

print("\n🎉 Все специальности добавлены!")