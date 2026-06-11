from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Subject
from departments.models import Department


@login_required
def subject_list(request):
    subjects = Subject.objects.all().select_related('department')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        subjects = subjects.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )

    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        subjects = subjects.filter(department__id=department_filter)

    # Filter by subject type
    type_filter = request.GET.get('type', '')
    if type_filter:
        subjects = subjects.filter(subject_type=type_filter)

    # Filter by semester
    semester_filter = request.GET.get('semester', '')
    if semester_filter:
        subjects = subjects.filter(semester=semester_filter)

    # Pagination
    paginator = Paginator(subjects, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics
    total_credits = subjects.aggregate(total=Sum('credits'))['total'] or 0
    total_hours = subjects.aggregate(total=Sum('total_hours'))['total'] or 0

    context = {
        'subjects': page_obj,
        'total_count': subjects.count(),
        'total_credits': total_credits,
        'total_hours': total_hours,
        'search_query': search_query,
        'department_filter': department_filter,
        'type_filter': type_filter,
        'semester_filter': semester_filter,
        'departments': Department.objects.all(),
        'subject_types': Subject.SUBJECT_TYPES,
        'semesters': Subject.SEMESTER_CHOICES,
    }
    return render(request, 'subjects/list.html', context)


@login_required
def subject_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        department_id = request.POST.get('department')
        subject_type = request.POST.get('subject_type')
        semester = request.POST.get('semester')
        credits = request.POST.get('credits', 0)
        total_hours = request.POST.get('total_hours', 0)
        lecture_hours = request.POST.get('lecture_hours', 0)
        practical_hours = request.POST.get('practical_hours', 0)
        lab_hours = request.POST.get('lab_hours', 0)
        exam_type = request.POST.get('exam_type')
        description = request.POST.get('description', '')

        # Validation
        if not all([name, code, department_id, subject_type, semester, exam_type]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'subjects/form.html', {
                'title': "Fan qo'shish",
                'departments': Department.objects.all(),
                'subject_types': Subject.SUBJECT_TYPES,
                'semesters': Subject.SEMESTER_CHOICES,
                'exam_types': Subject.EXAM_TYPES,
            })

        if Subject.objects.filter(code=code).exists():
            messages.error(request, f"'{code}' kodi bilan fan allaqachon mavjud!")
            return render(request, 'subjects/form.html', {
                'title': "Fan qo'shish",
                'departments': Department.objects.all(),
                'subject_types': Subject.SUBJECT_TYPES,
                'semesters': Subject.SEMESTER_CHOICES,
                'exam_types': Subject.EXAM_TYPES,
            })

        department = get_object_or_404(Department, id=department_id)
        subject = Subject.objects.create(
            name=name,
            code=code,
            department=department,
            subject_type=subject_type,
            semester=semester,
            credits=credits,
            total_hours=total_hours,
            lecture_hours=lecture_hours,
            practical_hours=practical_hours,
            lab_hours=lab_hours,
            exam_type=exam_type,
            description=description
        )
        messages.success(request, f"'{subject.name}' fani muvaffaqiyatli qo'shildi!")
        return redirect('subject_list')

    context = {
        'title': "Fan qo'shish",
        'departments': Department.objects.all(),
        'subject_types': Subject.SUBJECT_TYPES,
        'semesters': Subject.SEMESTER_CHOICES,
        'exam_types': Subject.EXAM_TYPES,
    }
    return render(request, 'subjects/form.html', context)


@login_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        old_name = subject.name
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        department_id = request.POST.get('department')
        subject.subject_type = request.POST.get('subject_type')
        subject.semester = request.POST.get('semester')
        subject.credits = request.POST.get('credits', 0)
        subject.total_hours = request.POST.get('total_hours', 0)
        subject.lecture_hours = request.POST.get('lecture_hours', 0)
        subject.practical_hours = request.POST.get('practical_hours', 0)
        subject.lab_hours = request.POST.get('lab_hours', 0)
        subject.exam_type = request.POST.get('exam_type')
        subject.description = request.POST.get('description', '')

        if department_id:
            subject.department = get_object_or_404(Department, id=department_id)

        subject.save()
        messages.success(request, f"'{old_name}' fani '{subject.name}' ga tahrirlandi!")
        return redirect('subject_list')

    context = {
        'subject': subject,
        'title': "Fan tahrirlash",
        'departments': Department.objects.all(),
        'subject_types': Subject.SUBJECT_TYPES,
        'semesters': Subject.SEMESTER_CHOICES,
        'exam_types': Subject.EXAM_TYPES,
    }
    return render(request, 'subjects/form.html', context)


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        subject_name = subject.name
        subject.delete()
        messages.success(request, f"'{subject_name}' fani o'chirildi!")
        return redirect('subject_list')

    return render(request, 'subjects/delete.html', {'subject': subject})


@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    context = {
        'subject': subject,
    }
    return render(request, 'subjects/detail.html', context)