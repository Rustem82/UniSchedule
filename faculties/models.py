from django.db import models
from django.urls import reverse


class Faculty(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nomi")
    code = models.CharField(max_length=20, unique=True, verbose_name="Kodi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    dean_name = models.CharField(max_length=255, blank=True, verbose_name="Dekan ismi")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    established_date = models.DateField(null=True, blank=True, verbose_name="Tashkil etilgan sana")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def get_absolute_url(self):
        return reverse('faculties:detail', args=[str(self.id)])