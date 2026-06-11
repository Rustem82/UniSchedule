from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', "Yaratish"),
        ('update', "Tahrirlash"),
        ('delete', "O'chirish"),
        ('view', "Ko'rish"),
        ('export', "Eksport"),
        ('login', "Kirish"),
        ('logout', "Chiqish"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs', verbose_name="Foydalanuvchi")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, verbose_name="Harakat")
    model_name = models.CharField(max_length=100, verbose_name="Model nomi")
    object_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="Ob'ekt ID")
    object_repr = models.CharField(max_length=200, blank=True, verbose_name="Ob'ekt nomi")
    changes = models.TextField(blank=True, verbose_name="O'zgarishlar")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP manzil")
    user_agent = models.CharField(max_length=500, blank=True, verbose_name="Brauzer ma'lumoti")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Vaqt")

    class Meta:
        verbose_name = "Audit log"
        verbose_name_plural = "Audit loglari"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.get_action_display()} - {self.model_name}"