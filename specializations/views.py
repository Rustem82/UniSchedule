from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Specialization
from faculties.models import Faculty


@login_required
def specialization_list(request):
    specializations = Specialization.objects.all().select_related('faculty')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        specializations = specializations.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(faculty__name__icontains=search_query)
        )

    # Filter by faculty
    faculty_filter = request.GET.get('faculty', '')
    if faculty_filter:
        specializations = specializations.filter(faculty__id=faculty_filter)

    # Filter by degree
    degree_filter = request.GET.get('degree', '')
    if degree_filter:
        specializations = specializations.filter(degree_type=degree_filter)

    # Filter by education type
    education_filter = request.GET.get('education', '')
    if education_filter:
        specializations = specializations.filter(education_type=education_filter)

    # Pagination
    paginator = Paginator(specializations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'specializations': page_obj,
        'total_count': specializations.count(),
        'search_query': search_query,
        'faculty_filter': faculty_filter,
        'degree_filter': degree_filter,
        'education_filter': education_filter,
        'faculties': Faculty.objects.all(),
        'degree_types': Specialization.DEGREE_TYPES,
        'education_types': Specialization.EDUCATION_TYPES,
    }
    return render(request, 'specializations/list.html', context)


@login_required
def specialization_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        faculty_id = request.POST.get('faculty')
        degree_type = request.POST.get('degree_type')
        education_type = request.POST.get('education_type')
        duration = request.POST.get('duration')
        credits = request.POST.get('credits', 0)
        description = request.POST.get('description', '')

        # Validation
        if not all([name, code, faculty_id, degree_type, education_type, duration]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'specializations/form.html', {
                'title': 'Mutaxassislik qo\'shish',
                'faculties': Faculty.objects.all(),
                'degree_types': Specialization.DEGREE_TYPES,
                'education_types': Specialization.EDUCATION_TYPES,
            })

        if Specialization.objects.filter(code=code).exists():
            messages.error(request, f"'{code}' kodi bilan mutaxassislik allaqachon mavjud!")
            return render(request, 'specializations/form.html', {
                'title': 'Mutaxassislik qo\'shish',
                'faculties': Faculty.objects.all(),
                'degree_types': Specialization.DEGREE_TYPES,
                'education_types': Specialization.EDUCATION_TYPES,
            })

        faculty = get_object_or_404(Faculty, id=faculty_id)
        specialization = Specialization.objects.create(
            name=name,
            code=code,
            faculty=faculty,
            degree_type=degree_type,
            education_type=education_type,
            duration=duration,
            credits=credits,
            description=description
        )
        messages.success(request, f"'{specialization.name}' mutaxassisligi muvaffaqiyatli qo'shildi!")
        return redirect('specialization_list')

    context = {
        'title': 'Mutaxassislik qo\'shish',
        'faculties': Faculty.objects.all(),
        'degree_types': Specialization.DEGREE_TYPES,
        'education_types': Specialization.EDUCATION_TYPES,
    }
    return render(request, 'specializations/form.html', context)


@login_required
def specialization_edit(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)

    if request.method == 'POST':
        old_name = specialization.name
        specialization.name = request.POST.get('name')
        specialization.code = request.POST.get('code')
        faculty_id = request.POST.get('faculty')
        specialization.degree_type = request.POST.get('degree_type')
        specialization.education_type = request.POST.get('education_type')
        specialization.duration = request.POST.get('duration')
        specialization.credits = request.POST.get('credits', 0)
        specialization.description = request.POST.get('description', '')

        if faculty_id:
            specialization.faculty = get_object_or_404(Faculty, id=faculty_id)

        specialization.save()
        messages.success(request, f"'{old_name}' mutaxassisligi '{specialization.name}' ga tahrirlandi!")
        return redirect('specialization_list')

    context = {
        'specialization': specialization,
        'title': 'Mutaxassislik tahrirlash',
        'faculties': Faculty.objects.all(),
        'degree_types': Specialization.DEGREE_TYPES,
        'education_types': Specialization.EDUCATION_TYPES,
    }
    return render(request, 'specializations/form.html', context)


@login_required
def specialization_delete(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)

    if request.method == 'POST':
        specialization_name = specialization.name
        specialization.delete()
        messages.success(request, f"'{specialization_name}' mutaxassisligi o'chirildi!")
        return redirect('specialization_list')

    return render(request, 'specializations/delete.html', {'specialization': specialization})


@login_required
def specialization_detail(request, pk):
    specialization = get_object_or_404(Specialization, pk=pk)
    groups = specialization.groups.all()

    context = {
        'specialization': specialization,
        'groups': groups,
    }
    return render(request, 'specializations/detail.html', context)