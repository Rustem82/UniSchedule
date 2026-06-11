from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import AcademicGroup
from specializations.models import Specialization
from faculties.models import Faculty


@login_required
def group_list(request):
    groups = AcademicGroup.objects.all().select_related('specialization__faculty')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        groups = groups.filter(
            Q(name__icontains=search_query) |
            Q(specialization__name__icontains=search_query) |
            Q(specialization__code__icontains=search_query)
        )

    # Filter by faculty
    faculty_filter = request.GET.get('faculty', '')
    if faculty_filter:
        groups = groups.filter(specialization__faculty__id=faculty_filter)

    # Filter by specialization
    spec_filter = request.GET.get('specialization', '')
    if spec_filter:
        groups = groups.filter(specialization__id=spec_filter)

    # Filter by course
    course_filter = request.GET.get('course', '')
    if course_filter:
        groups = groups.filter(current_course=course_filter)

    # Filter by language
    language_filter = request.GET.get('language', '')
    if language_filter:
        groups = groups.filter(language=language_filter)

    # Pagination
    paginator = Paginator(groups, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics
    total_students = groups.aggregate(total=Count('student_count'))['total'] or 0

    context = {
        'groups': page_obj,
        'total_count': groups.count(),
        'total_students': total_students,
        'search_query': search_query,
        'faculty_filter': faculty_filter,
        'spec_filter': spec_filter,
        'course_filter': course_filter,
        'language_filter': language_filter,
        'faculties': Faculty.objects.all(),
        'specializations': Specialization.objects.all(),
        'courses': AcademicGroup.COURSE_CHOICES,
        'languages': [('uzbek', "O'zbek"), ('russian', "Rus"), ('english', "Ingliz")],
    }
    return render(request, 'groups/list.html', context)


@login_required
def group_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        specialization_id = request.POST.get('specialization')
        year_of_admission = request.POST.get('year_of_admission')
        current_course = request.POST.get('current_course')
        student_count = request.POST.get('student_count', 0)
        language = request.POST.get('language')
        is_active = request.POST.get('is_active') == 'on'

        # Validation
        if not all([name, specialization_id, year_of_admission, current_course, language]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'groups/form.html', {
                'title': "Guruh qo'shish",
                'specializations': Specialization.objects.all(),
                'courses': AcademicGroup.COURSE_CHOICES,
                'languages': [('uzbek', "O'zbek"), ('russian', "Rus"), ('english', "Ingliz")],
            })

        if AcademicGroup.objects.filter(name=name, year_of_admission=year_of_admission).exists():
            messages.error(request, f"'{name}' guruhi {year_of_admission}-yilda allaqachon mavjud!")
            return render(request, 'groups/form.html', {
                'title': "Guruh qo'shish",
                'specializations': Specialization.objects.all(),
                'courses': AcademicGroup.COURSE_CHOICES,
                'languages': [('uzbek', "O'zbek"), ('russian', "Rus"), ('english', "Ingliz")],
            })

        specialization = get_object_or_404(Specialization, id=specialization_id)
        group = AcademicGroup.objects.create(
            name=name,
            specialization=specialization,
            year_of_admission=year_of_admission,
            current_course=current_course,
            student_count=student_count,
            language=language,
            is_active=is_active
        )
        messages.success(request, f"'{group.name}' guruhi muvaffaqiyatli qo'shildi!")
        return redirect('group_list')

    context = {
        'title': "Guruh qo'shish",
        'specializations': Specialization.objects.all(),
        'courses': AcademicGroup.COURSE_CHOICES,
        'languages': [('uzbek', "O'zbek"), ('russian', "Rus"), ('english', "Ingliz")],
    }
    return render(request, 'groups/form.html', context)


@login_required
def group_edit(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)

    if request.method == 'POST':
        old_name = group.name
        group.name = request.POST.get('name')
        specialization_id = request.POST.get('specialization')
        group.year_of_admission = request.POST.get('year_of_admission')
        group.current_course = request.POST.get('current_course')
        group.student_count = request.POST.get('student_count', 0)
        group.language = request.POST.get('language')
        group.is_active = request.POST.get('is_active') == 'on'

        if specialization_id:
            group.specialization = get_object_or_404(Specialization, id=specialization_id)

        group.save()
        messages.success(request, f"'{old_name}' guruhi '{group.name}' ga tahrirlandi!")
        return redirect('group_list')

    context = {
        'group': group,
        'title': "Guruh tahrirlash",
        'specializations': Specialization.objects.all(),
        'courses': AcademicGroup.COURSE_CHOICES,
        'languages': [('uzbek', "O'zbek"), ('russian', "Rus"), ('english', "Ingliz")],
    }
    return render(request, 'groups/form.html', context)


@login_required
def group_delete(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)

    if request.method == 'POST':
        group_name = group.name
        group.delete()
        messages.success(request, f"'{group_name}' guruhi o'chirildi!")
        return redirect('group_list')

    return render(request, 'groups/delete.html', {'group': group})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(AcademicGroup, pk=pk)

    context = {
        'group': group,
    }
    return render(request, 'groups/detail.html', context)