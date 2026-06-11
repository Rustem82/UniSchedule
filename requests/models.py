from django.db import models
from departments.models import Department
from subjects.models import Subject
from teachers.models import Teacher


class WorkloadRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', "Kutilmoqda"),
        ('sent', "Yuborilgan"),
        ('approved', "Tasdiqlangan"),
        ('rejected', "Rad etilgan"),
        ('completed', "Bajarilgan"),
        ('cancelled', "Bekor qilingan"),
    ]

    REQUEST_TYPES = [
        ('standard', "Standart"),
        ('urgent', "Shoshilinch"),
        ('exchange', "Almashuv"),
    ]

    from_department = models.ForeignKey(Department, related_name='sent_requests', on_delete=models.CASCADE,
                                        verbose_name="Jo'natuvchi kafedra")
    to_department = models.ForeignKey(Department, related_name='received_requests', on_delete=models.CASCADE,
                                      verbose_name="Qabul qiluvchi kafedra")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Fan")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="Taklif qilinayotgan o'qituvchi")
    semester = models.PositiveSmallIntegerField(verbose_name="Semestr")
    total_hours = models.PositiveIntegerField(verbose_name="Jami soatlar")
    lecture_hours = models.PositiveIntegerField(default=0, verbose_name="Ma'ruza soatlari")
    practical_hours = models.PositiveIntegerField(default=0, verbose_name="Amaliy soatlar")
    lab_hours = models.PositiveIntegerField(default=0, verbose_name="Laboratoriya soatlari")
    message = models.TextField(blank=True, verbose_name="Xabar")
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES, default='standard',
                                    verbose_name="Talabnoma turi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    rejection_reason = models.TextField(blank=True, verbose_name="Rad etish sababi")
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='created_requests',
                                   verbose_name="Yaratuvchi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_requests', verbose_name="Tasdiqlovchi")

    class Meta:
        verbose_name = "Talabnoma"
        verbose_name_plural = "Talabnomalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_department} → {self.to_department}: {self.subject} ({self.get_status_display()})"

    def get_total_hours_display(self):
        return f"{self.total_hours} soat"

    @property
    def is_urgent(self):
        return self.request_type == 'urgent'