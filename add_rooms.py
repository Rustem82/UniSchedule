import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'unischedule_project.settings')
django.setup()

from rooms.models import Building, Room

# Создаем здания
buildings = [
    {"name": "Asosiy bino", "code": "A", "address": "Markaziy ko'cha 1", "floors": 5},
    {"name": "O'quv binosi", "code": "B", "address": "Universitet ko'chasi 15", "floors": 4},
    {"name": "Laboratoriya binosi", "code": "C", "address": "Ilm-fan ko'chasi 8", "floors": 3},
]

for b in buildings:
    building, created = Building.objects.get_or_create(code=b["code"], defaults=b)
    print(f"{'✅ Создано' if created else 'ℹ️ Существует'} здание: {building.name}")

# Создаем комнаты
for building in Building.objects.all():
    for floor in range(1, building.floors + 1):
        for num in range(101, 105):
            room, created = Room.objects.get_or_create(
                building=building, number=f"{floor}{num}",
                defaults={"capacity": 50, "room_type": "lecture", "floor": floor, "has_whiteboard": True}
            )
            if created:
                print(f"✅ Создана комната: {room}")