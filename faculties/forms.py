from django import forms
from .models import Faculty

class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'code', 'description', 'dean_name', 'phone', 'email', 'established_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fakultet nomi'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: AF'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Qisqacha tavsif'}),
            'dean_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dekan ismi'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+998 XX XXX-XX-XX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'fakultet@example.com'}),
            'established_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }