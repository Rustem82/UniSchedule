from django.db import models
from groups.models import AcademicGroup
from subjects.models import Subject
from teachers.models import Teacher
from rooms.models import Room


class Schedule(models.Model):
    WEEKDAYS = [
        (1, "Dushanba"),
        (2, "Seshanba"),
        (3, "Chorshanba"),
        (4, "Payshanba"),
        (5, "Juma"),
        (6, "Shanba"),
    ]

    LESSON_TYPES = [
        ('lecture', "Ma'ruza"),
        ('practical', "Amaliy"),
        ('lab', "Laboratoriya"),
        ('seminar', "Seminar"),
    ]

    LESSON_TIMES = [
        (1, "08:30 - 10:00"),
        (2, "10:10 - 11:40"),
        (3, "11:50 - 13:20"),
        (4, "13:30 - 15:00"),
        (5, "15:10 - 16:40"),
        (6, "16:50 - 18:20"),
        (7, "18:30 - 20:00"),
    ]

    WEEK_TYPES = [
        ('all', "Har hafta"),
        ('odd', "Toq haftalar"),
        ('even', "Juft haftalar"),
    ]

    group = models.ForeignKey(AcademicGroup, on_delete=models.CASCADE, related_name='schedules', verbose_name="Guruh")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="O'qituvchi")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Xona")
    day_of_week = models.PositiveSmallIntegerField(choices=WEEKDAYS, verbose_name="Hafta kuni")
    lesson_number = models.PositiveSmallIntegerField(choices=LESSON_TIMES, verbose_name="Juftlik")
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, verbose_name="Dars turi")
    week_type = models.CharField(max_length=10, choices=WEEK_TYPES, default='all', verbose_name="Hafta turi")
    subgroup = models.PositiveSmallIntegerField(default=1, verbose_name="Podgruppa")
    academic_year = models.CharField(max_length=9, verbose_name="O'quv yili")
    semester = models.PositiveSmallIntegerField(verbose_name="Semestr")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dars jadvali"
        verbose_name_plural = "Dars jadvallari"
        ordering = ['day_of_week', 'lesson_number', 'group__name']
        unique_together = ['group', 'day_of_week', 'lesson_number', 'week_type']

    def __str__(self):
        return f"{self.group.name} - {self.subject.name} - {self.get_day_of_week_display()} ({self.get_lesson_number_display()})"

    def get_lesson_time_display(self):
        return dict(self.LESSON_TIMES).get(self.lesson_number, "")