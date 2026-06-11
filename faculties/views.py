from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Faculty
from departments.models import Department
from teachers.models import Teacher


@login_required
def faculty_list(request):
    faculties = Faculty.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        faculties = faculties.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(faculties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'faculties': page_obj,
        'total_count': faculties.count(),
        'search_query': search_query,
    }
    return render(request, 'faculties/list.html', context)


@login_required
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    departments = faculty.departments.all()
    specializations = faculty.specializations.all()
    teachers = Teacher.objects.filter(department__faculty=faculty).select_related('user', 'department')

    context = {
        'faculty': faculty,
        'departments': departments,
        'specializations': specializations,
        'teachers': teachers,
    }
    return render(request, 'faculties/detail.html', context)


@login_required
def faculty_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description', '')
        dean_name = request.POST.get('dean_name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')

        if Faculty.objects.filter(code=code).exists():
            messages.error(request, f"'{code}' kodi bilan fakultet allaqachon mavjud!")
            return render(request, 'faculties/form.html', {'title': 'Fakultet qo\'shish'})

        faculty = Faculty.objects.create(
            name=name,
            code=code,
            description=description,
            dean_name=dean_name,
            phone=phone,
            email=email
        )
        messages.success(request, f"'{faculty.name}' fakulteti muvaffaqiyatli qo'shildi!")
        return redirect('faculty_list')

    return render(request, 'faculties/form.html', {'title': 'Fakultet qo\'shish'})


@login_required
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)

    if request.method == 'POST':
        old_name = faculty.name
        faculty.name = request.POST.get('name')
        faculty.code = request.POST.get('code')
        faculty.description = request.POST.get('description', '')
        faculty.dean_name = request.POST.get('dean_name', '')
        faculty.phone = request.POST.get('phone', '')
        faculty.email = request.POST.get('email', '')
        faculty.save()

        messages.success(request, f"'{old_name}' fakulteti '{faculty.name}' ga tahrirlandi!")
        return redirect('faculty_list')

    context = {
        'faculty': faculty,
        'title': 'Fakultet tahrirlash'
    }
    return render(request, 'faculties/form.html', context)


@login_required
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)

    if request.method == 'POST':
        faculty_name = faculty.name
        faculty.delete()
        messages.success(request, f"'{faculty_name}' fakulteti o'chirildi!")
        return redirect('faculty_list')

    return render(request, 'faculties/delete.html', {'faculty': faculty})