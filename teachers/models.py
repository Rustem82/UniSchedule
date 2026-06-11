from django.db import models
from django.contrib.auth.models import User
from departments.models import Department


class Teacher(models.Model):
    ACADEMIC_DEGREES = [
        ('none', "Yo'q"),
        ('phd', "PhD"),
        ('dsc', "DSc"),
        ('professor', "Professor"),
    ]

    POSITIONS = [
        ('teacher', "O'qituvchi"),
        ('senior_teacher', "Katta o'qituvchi"),
        ('docent', "Dotsent"),
        ('professor', "Professor"),
        ('head', "Kafedra mudiri"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile',
                                verbose_name="Foydalanuvchi")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='teachers',
                                   verbose_name="Kafedra")
    academic_degree = models.CharField(max_length=20, choices=ACADEMIC_DEGREES, default='none',
                                       verbose_name="Ilmiy daraja")
    position = models.CharField(max_length=20, choices=POSITIONS, default='teacher', verbose_name="Lavozim")
    employee_id = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Xodim ID")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    address = models.TextField(blank=True, verbose_name="Manzil")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    start_date = models.DateField(null=True, blank=True, verbose_name="Ish boshlagan sana")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "O'qituvchi"
        verbose_name_plural = "O'qituvchilar"
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    def get_full_name(self):
        return self.user.get_full_name()

    def get_full_info(self):
        return f"{self.get_full_name()} - {self.get_position_display()}"