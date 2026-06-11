from django.db import models


class Building(models.Model):
    name = models.CharField(max_length=100, verbose_name="Bino nomi")
    code = models.CharField(max_length=20, unique=True, verbose_name="Bino kodi")
    address = models.CharField(max_length=255, verbose_name="Manzil")
    floors = models.PositiveSmallIntegerField(default=0, verbose_name="Qavatlar soni")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bino"
        verbose_name_plural = "Binolar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_rooms_count(self):
        return self.rooms.count()


class Room(models.Model):
    ROOM_TYPES = [
        ('lecture', "Ma'ruza xonasi"),
        ('seminar', "Seminar xonasi"),
        ('lab', "Laboratoriya"),
        ('computer', "Kompyuter xonasi"),
        ('conference', "Konferensiya zali"),
        ('office', "Ofis"),
        ('library', "Kutubxona"),
        ('sport', "Sport zali"),
    ]

    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='rooms', verbose_name="Bino")
    number = models.CharField(max_length=20, verbose_name="Xona raqami")
    capacity = models.PositiveSmallIntegerField(default=0, verbose_name="Sig'imi")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='lecture', verbose_name="Xona turi")
    floor = models.PositiveSmallIntegerField(default=1, verbose_name="Qavat")
    has_projector = models.BooleanField(default=False, verbose_name="Proyektor")
    has_computer = models.BooleanField(default=False, verbose_name="Kompyuter")
    has_whiteboard = models.BooleanField(default=True, verbose_name="Doska")
    has_air_conditioner = models.BooleanField(default=False, verbose_name="Konditsioner")
    has_wifi = models.BooleanField(default=False, verbose_name="Wi-Fi")
    is_available = models.BooleanField(default=True, verbose_name="Mavjud")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Xona"
        verbose_name_plural = "Xonalar"
        ordering = ['building__name', 'floor', 'number']
        unique_together = ['building', 'number']

    def __str__(self):
        return f"{self.building.code} - {self.number} ({self.get_room_type_display()})"

    def get_equipment_list(self):
        equipment = []
        if self.has_projector:
            equipment.append("Proyektor")
        if self.has_computer:
            equipment.append("Kompyuter")
        if self.has_whiteboard:
            equipment.append("Doska")
        if self.has_air_conditioner:
            equipment.append("Konditsioner")
        if self.has_wifi:
            equipment.append("Wi-Fi")
        return equipment