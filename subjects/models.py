from django.db import models
from departments.models import Department


class Subject(models.Model):
    SUBJECT_TYPES = [
        ('general', "Umumiy"),
        ('core', "Asosiy"),
        ('elective', "Tanlov"),
        ('professional', "Professional"),
    ]

    SEMESTER_CHOICES = [(i, f"{i}-semestr") for i in range(1, 9)]

    EXAM_TYPES = [
        ('exam', "Imtihon"),
        ('test', "Test"),
        ('project', "Loyiha"),
        ('coursework', "Kurs ishi"),
    ]

    name = models.CharField(max_length=255, verbose_name="Fan nomi")
    code = models.CharField(max_length=20, unique=True, verbose_name="Fan kodi")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects',
                                   verbose_name="Kafedra")
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES, default='core', verbose_name="Fan turi")
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, verbose_name="Semestr")
    credits = models.PositiveSmallIntegerField(default=0, verbose_name="Kreditlar")
    total_hours = models.PositiveIntegerField(default=0, verbose_name="Jami soatlar")
    lecture_hours = models.PositiveIntegerField(default=0, verbose_name="Ma'ruza soatlari")
    practical_hours = models.PositiveIntegerField(default=0, verbose_name="Amaliy soatlar")
    lab_hours = models.PositiveIntegerField(default=0, verbose_name="Laboratoriya soatlari")
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='exam', verbose_name="Imtihon turi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar bazasi"
        ordering = ['department__name', 'semester', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def remaining_hours(self):
        return self.lecture_hours + self.practical_hours + self.lab_hours