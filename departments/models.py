from django.db import models
from faculties.models import Faculty


class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    code = models.CharField(max_length=20, unique=True, verbose_name="Kodi")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments', verbose_name="Fakultet")
    head_name = models.CharField(max_length=255, blank=True, verbose_name="Kafedra mudiri")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kafedra"
        verbose_name_plural = "Kafedralar"
        ordering = ['faculty__name', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_teacher_count(self):
        return self.teachers.count()