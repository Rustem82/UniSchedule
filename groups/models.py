from django.db import models
from specializations.models import Specialization


class AcademicGroup(models.Model):
    COURSE_CHOICES = [(i, f"{i}-kurs") for i in range(1, 5)]

    name = models.CharField(max_length=50, unique=True, verbose_name="Guruh nomi")
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, related_name='groups',
                                       verbose_name="Mutaxassislik")
    year_of_admission = models.PositiveSmallIntegerField(verbose_name="Qabul yili")
    current_course = models.PositiveSmallIntegerField(choices=COURSE_CHOICES, default=1, verbose_name="Kurs")
    student_count = models.PositiveSmallIntegerField(default=0, verbose_name="Talabalar soni")
    language = models.CharField(max_length=20, choices=[('uzbek', "O'zbek"), ('russian', "Rus"), ('english', "Ingliz")],
                                default='uzbek', verbose_name="Ta'lim tili")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Akademik guruh"
        verbose_name_plural = "Akademik guruhlar"
        ordering = ['specialization__faculty__name', 'specialization__name', 'name']
        unique_together = ['name', 'year_of_admission']

    def __str__(self):
        return f"{self.name} ({self.specialization.code})"

    def get_full_info(self):
        return f"{self.name} - {self.specialization.name} ({self.year_of_admission})"