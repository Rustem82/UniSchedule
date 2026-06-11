from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Department
from faculties.models import Faculty


@login_required
def department_list(request):
    departments = Department.objects.all().select_related('faculty')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(faculty__name__icontains=search_query)
        )

    # Filter by faculty
    faculty_filter = request.GET.get('faculty', '')
    if faculty_filter:
        departments = departments.filter(faculty__id=faculty_filter)

    # Pagination
    paginator = Paginator(departments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'departments': page_obj,
        'total_count': departments.count(),
        'search_query': search_query,
        'faculty_filter': faculty_filter,
        'faculties': Faculty.objects.all(),
    }
    return render(request, 'departments/list.html', context)


@login_required
def department_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        faculty_id = request.POST.get('faculty')
        head_name = request.POST.get('head_name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        description = request.POST.get('description', '')

        # Validation
        if not name or not code or not faculty_id:
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'departments/form.html', {
                'title': 'Kafedra qo\'shish',
                'faculties': Faculty.objects.all()
            })

        if Department.objects.filter(code=code).exists():
            messages.error(request, f"'{code}' kodi bilan kafedra allaqachon mavjud!")
            return render(request, 'departments/form.html', {
                'title': 'Kafedra qo\'shish',
                'faculties': Faculty.objects.all()
            })

        faculty = get_object_or_404(Faculty, id=faculty_id)
        department = Department.objects.create(
            name=name,
            code=code,
            faculty=faculty,
            head_name=head_name,
            phone=phone,
            email=email,
            description=description
        )
        messages.success(request, f"'{department.name}' kafedrasi muvaffaqiyatli qo'shildi!")
        return redirect('department_list')

    context = {
        'title': 'Kafedra qo\'shish',
        'faculties': Faculty.objects.all(),
    }
    return render(request, 'departments/form.html', context)


@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        old_name = department.name
        department.name = request.POST.get('name')
        department.code = request.POST.get('code')
        faculty_id = request.POST.get('faculty')
        department.head_name = request.POST.get('head_name', '')
        department.phone = request.POST.get('phone', '')
        department.email = request.POST.get('email', '')
        department.description = request.POST.get('description', '')

        if faculty_id:
            department.faculty = get_object_or_404(Faculty, id=faculty_id)

        department.save()
        messages.success(request, f"'{old_name}' kafedrasi '{department.name}' ga tahrirlandi!")
        return redirect('department_list')

    context = {
        'department': department,
        'title': 'Kafedra tahrirlash',
        'faculties': Faculty.objects.all(),
    }
    return render(request, 'departments/form.html', context)


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == 'POST':
        department_name = department.name
        department.delete()
        messages.success(request, f"'{department_name}' kafedrasi o'chirildi!")
        return redirect('department_list')

    return render(request, 'departments/delete.html', {'department': department})


@login_required
def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    teachers = department.teachers.all()

    context = {
        'department': department,
        'teachers': teachers,
    }
    return render(request, 'departments/detail.html', context)