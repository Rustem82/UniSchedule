from django.db import models
from teachers.models import Teacher
from subjects.models import Subject
from groups.models import AcademicGroup


class Workload(models.Model):
    SEMESTER_CHOICES = [(i, f"{i}-semestr") for i in range(1, 9)]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='workloads', verbose_name="O'qituvchi")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='workloads', verbose_name="Fan")
    group = models.ForeignKey(AcademicGroup, on_delete=models.CASCADE, related_name='workloads', verbose_name="Guruh")
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES, verbose_name="Semestr")
    lecture_hours = models.PositiveIntegerField(default=0, verbose_name="Ma'ruza soatlari")
    practical_hours = models.PositiveIntegerField(default=0, verbose_name="Amaliy soatlar")
    lab_hours = models.PositiveIntegerField(default=0, verbose_name="Laboratoriya soatlari")
    independent_hours = models.PositiveIntegerField(default=0, verbose_name="Mustaqil ta'lim")
    academic_year = models.CharField(max_length=9, verbose_name="O'quv yili")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O'quv yuklamasi"
        verbose_name_plural = "O'quv yuklamalari"
        unique_together = ['teacher', 'subject', 'group', 'semester', 'academic_year']
        ordering = ['-academic_year', 'teacher__user__last_name', 'semester']

    @property
    def total_hours(self):
        return self.lecture_hours + self.practical_hours + self.lab_hours + self.independent_hours

    def __str__(self):
        return f"{self.teacher} - {self.subject} ({self.group}) - {self.semester}-semestr"