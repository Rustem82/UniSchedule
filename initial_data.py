import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from faculties.models import Faculty
from django.contrib.auth.models import User

# Создание факультетов
faculties_data = [
    {"name": "Amaliy fanlar fakulteti", "code": "AF", "description": "Amaliy fanlar fakulteti"},
    {"name": "Sharq sivilizatsiyasi va falsafa fakulteti", "code": "SHF", "description": "Sharq sivilizatsiyasi va falsafa fakulteti"},
    {"name": "Sharq xalqlari tillari va adabiyoti instituti", "code": "SHXTAI", "description": "Sharq xalqlari tillari va adabiyoti instituti"},
    {"name": "Tashqi siyosat va xalqaro iqtisodiy munosabatlar instituti", "code": "TSXIM", "description": "Tashqi siyosat va xalqaro iqtisodiy munosabatlar instituti"},
]

for faculty_data in faculties_data:
    Faculty.objects.get_or_create(code=faculty_data["code"], defaults=faculty_data)

print("✅ Fakultetlar muvaffaqiyatli qo'shildi!")

# Создание администратора, если не существует
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Admin foydalanuvchi yaratildi (login: admin, parol: admin123)")