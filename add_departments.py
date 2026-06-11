import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from departments.models import Department
from faculties.models import Faculty

# Получаем факультеты
af = Faculty.objects.get(code='AF')
shf = Faculty.objects.get(code='SHF')
shxtai = Faculty.objects.get(code='SHXTAI')
tsxim = Faculty.objects.get(code='TSXIM')

departments = [
    {"name": "Axborot texnologiyalari kafedrasi", "code": "AT", "faculty": af, "head_name": "Prof. Karimov A."},
    {"name": "Matematik fanlar kafedrasi", "code": "MF", "faculty": af, "head_name": "Prof. Rahimov B."},
    {"name": "Falsafa kafedrasi", "code": "FAL", "faculty": shf, "head_name": "Dots. Nazarov C."},
    {"name": "Siyosatshunoslik kafedrasi", "code": "SIY", "faculty": shf, "head_name": "Prof. Ismailov D."},
    {"name": "Sharq tillari kafedrasi", "code": "ST", "faculty": shxtai, "head_name": "Dots. Tursunov E."},
    {"name": "Sharq adabiyoti kafedrasi", "code": "SA", "faculty": shxtai, "head_name": "Prof. Alimova F."},
    {"name": "Xalqaro munosabatlar kafedrasi", "code": "XM", "faculty": tsxim, "head_name": "Prof. Usmanov G."},
    {"name": "Iqtisodiyot kafedrasi", "code": "IQT", "faculty": tsxim, "head_name": "Dots. Khasanov H."},
]

for dept in departments:
    d, created = Department.objects.get_or_create(
        code=dept["code"],
        defaults=dept
    )
    print(f"{'✅ Создана' if created else 'ℹ️ Существует'} кафедра: {d.name}")

print("\n🎉 Все кафедры добавлены!")