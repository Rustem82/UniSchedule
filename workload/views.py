from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum, F
from .models import Workload
from teachers.models import Teacher
from subjects.models import Subject
from groups.models import AcademicGroup
from departments.models import Department


@login_required
def workload_list(request):
    workloads = Workload.objects.all().select_related('teacher', 'subject', 'group')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        workloads = workloads.filter(
            Q(teacher__user__first_name__icontains=search_query) |
            Q(teacher__user__last_name__icontains=search_query) |
            Q(subject__name__icontains=search_query) |
            Q(group__name__icontains=search_query)
        )

    # Filter by teacher
    teacher_filter = request.GET.get('teacher', '')
    if teacher_filter:
        workloads = workloads.filter(teacher__id=teacher_filter)

    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        workloads = workloads.filter(teacher__department__id=department_filter)

    # Filter by academic year
    year_filter = request.GET.get('year', '')
    if year_filter:
        workloads = workloads.filter(academic_year=year_filter)

    # Filter by semester
    semester_filter = request.GET.get('semester', '')
    if semester_filter:
        workloads = workloads.filter(semester=semester_filter)

    # Pagination
    paginator = Paginator(workloads, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics - используем поля базы данных, а не property
    total_lecture_hours = workloads.aggregate(total=Sum('lecture_hours'))['total'] or 0
    total_practical_hours = workloads.aggregate(total=Sum('practical_hours'))['total'] or 0
    total_lab_hours = workloads.aggregate(total=Sum('lab_hours'))['total'] or 0
    total_independent_hours = workloads.aggregate(total=Sum('independent_hours'))['total'] or 0

    # Вычисляем общее количество часов
    all_workloads = workloads
    total_hours = 0
    for w in all_workloads:
        total_hours += w.total_hours

    context = {
        'workloads': page_obj,
        'total_count': workloads.count(),
        'total_lecture_hours': total_lecture_hours,
        'total_practical_hours': total_practical_hours,
        'total_lab_hours': total_lab_hours,
        'total_independent_hours': total_independent_hours,
        'total_hours': total_hours,
        'search_query': search_query,
        'teacher_filter': teacher_filter,
        'department_filter': department_filter,
        'year_filter': year_filter,
        'semester_filter': semester_filter,
        'teachers': Teacher.objects.filter(is_active=True),
        'departments': Department.objects.all(),
        'academic_years': Workload.objects.values_list('academic_year', flat=True).distinct().order_by(
            '-academic_year'),
        'semesters': Workload.SEMESTER_CHOICES,
    }
    return render(request, 'workload/list.html', context)


@login_required
def workload_create(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        subject_id = request.POST.get('subject')
        group_id = request.POST.get('group')
        semester = request.POST.get('semester')
        lecture_hours = request.POST.get('lecture_hours', 0)
        practical_hours = request.POST.get('practical_hours', 0)
        lab_hours = request.POST.get('lab_hours', 0)
        independent_hours = request.POST.get('independent_hours', 0)
        academic_year = request.POST.get('academic_year')
        notes = request.POST.get('notes', '')

        if not all([teacher_id, subject_id, group_id, semester, academic_year]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'workload/form.html', {
                'title': "O'quv yuklamasi qo'shish",
                'teachers': Teacher.objects.filter(is_active=True),
                'subjects': Subject.objects.all(),
                'groups': AcademicGroup.objects.filter(is_active=True),
                'semesters': Workload.SEMESTER_CHOICES,
            })

        # Check for duplicate
        if Workload.objects.filter(
                teacher_id=teacher_id,
                subject_id=subject_id,
                group_id=group_id,
                semester=semester,
                academic_year=academic_year
        ).exists():
            messages.error(request, "Bu yuklama allaqachon mavjud!")
            return render(request, 'workload/form.html', {
                'title': "O'quv yuklamasi qo'shish",
                'teachers': Teacher.objects.filter(is_active=True),
                'subjects': Subject.objects.all(),
                'groups': AcademicGroup.objects.filter(is_active=True),
                'semesters': Workload.SEMESTER_CHOICES,
            })

        workload = Workload.objects.create(
            teacher_id=teacher_id,
            subject_id=subject_id,
            group_id=group_id,
            semester=semester,
            lecture_hours=int(lecture_hours),
            practical_hours=int(practical_hours),
            lab_hours=int(lab_hours),
            independent_hours=int(independent_hours),
            academic_year=academic_year,
            notes=notes
        )
        messages.success(request, f"Yuklama muvaffaqiyatli qo'shildi! Jami {workload.total_hours} soat")
        return redirect('workload_list')

    context = {
        'title': "O'quv yuklamasi qo'shish",
        'teachers': Teacher.objects.filter(is_active=True),
        'subjects': Subject.objects.all(),
        'groups': AcademicGroup.objects.filter(is_active=True),
        'semesters': Workload.SEMESTER_CHOICES,
    }
    return render(request, 'workload/form.html', context)


@login_required
def workload_edit(request, pk):
    workload = get_object_or_404(Workload, pk=pk)

    if request.method == 'POST':
        workload.teacher_id = request.POST.get('teacher')
        workload.subject_id = request.POST.get('subject')
        workload.group_id = request.POST.get('group')
        workload.semester = request.POST.get('semester')
        workload.lecture_hours = int(request.POST.get('lecture_hours', 0))
        workload.practical_hours = int(request.POST.get('practical_hours', 0))
        workload.lab_hours = int(request.POST.get('lab_hours', 0))
        workload.independent_hours = int(request.POST.get('independent_hours', 0))
        workload.academic_year = request.POST.get('academic_year')
        workload.notes = request.POST.get('notes', '')
        workload.save()

        messages.success(request, f"Yuklama tahrirlandi! Jami {workload.total_hours} soat")
        return redirect('workload_list')

    context = {
        'workload': workload,
        'title': "O'quv yuklamasi tahrirlash",
        'teachers': Teacher.objects.filter(is_active=True),
        'subjects': Subject.objects.all(),
        'groups': AcademicGroup.objects.filter(is_active=True),
        'semesters': Workload.SEMESTER_CHOICES,
    }
    return render(request, 'workload/form.html', context)


@login_required
def workload_delete(request, pk):
    workload = get_object_or_404(Workload, pk=pk)
    if request.method == 'POST':
        workload.delete()
        messages.success(request, "Yuklama o'chirildi!")
        return redirect('workload_list')
    return render(request, 'workload/delete.html', {'workload': workload})


@login_required
def workload_detail(request, pk):
    workload = get_object_or_404(Workload, pk=pk)
    return render(request, 'workload/detail.html', {'workload': workload})


@login_required
def workload_teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    workloads = Workload.objects.filter(teacher=teacher).select_related('subject', 'group')

    # Group by semester
    by_semester = {}
    for w in workloads:
        if w.semester not in by_semester:
            by_semester[w.semester] = []
        by_semester[w.semester].append(w)

    # Calculate totals
    total_hours = 0
    for w in workloads:
        total_hours += w.total_hours

    context = {
        'teacher': teacher,
        'by_semester': by_semester,
        'total_hours': total_hours,
        'workload_count': workloads.count(),
    }
    return render(request, 'workload/teacher_workload.html', context)


@login_required
def workload_summary(request):
    # Summary by department
    departments = Department.objects.all()
    summary_data = []

    for dept in departments:
        workloads = Workload.objects.filter(teacher__department=dept)
        total_hours = 0
        for w in workloads:
            total_hours += w.total_hours
        teacher_count = workloads.values('teacher').distinct().count()

        summary_data.append({
            'department': dept,
            'total_hours': total_hours,
            'teacher_count': teacher_count,
            'workload_count': workloads.count(),
        })

    total_overall_hours = sum(d['total_hours'] for d in summary_data)

    context = {
        'summary_data': summary_data,
        'total_overall_hours': total_overall_hours,
    }
    return render(request, 'workload/summary.html', context)