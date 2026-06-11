from django.db import models
from faculties.models import Faculty


class Specialization(models.Model):
    EDUCATION_TYPES = [
        ('kunduzgi', 'Kunduzgi'),
        ('sirtqi', 'Sirtqi'),
        ('kechki', 'Kechki'),
        ('masofaviy', 'Masofaviy'),
    ]

    DEGREE_TYPES = [
        ('bakalavr', 'Bakalavr'),
        ('magistr', 'Magistr'),
        ('doktorantura', 'Doktorantura'),
    ]

    name = models.CharField(max_length=255, verbose_name="Mutaxassislik nomi")
    code = models.CharField(max_length=20, unique=True, verbose_name="Kodi")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='specializations',
                                verbose_name="Fakultet")
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES, default='bakalavr', verbose_name="Daraja")
    education_type = models.CharField(max_length=20, choices=EDUCATION_TYPES, verbose_name="Ta'lim shakli")
    duration = models.PositiveSmallIntegerField(help_text="Muddat (oylarda)", verbose_name="Muddat")
    credits = models.PositiveSmallIntegerField(default=0, verbose_name="Kreditlar")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mutaxassislik"
        verbose_name_plural = "Mutaxassisliklar"
        ordering = ['faculty__name', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_group_count(self):
        return self.groups.count()