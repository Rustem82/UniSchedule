from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Schedule
from groups.models import AcademicGroup
from subjects.models import Subject
from teachers.models import Teacher
from rooms.models import Room


@login_required
def schedule_list(request):
    schedules = Schedule.objects.all().select_related('group', 'subject', 'teacher', 'room')

    # Filter by group
    group_filter = request.GET.get('group', '')
    if group_filter:
        schedules = schedules.filter(group__id=group_filter)

    # Filter by day
    day_filter = request.GET.get('day', '')
    if day_filter:
        schedules = schedules.filter(day_of_week=day_filter)

    # Filter by teacher
    teacher_filter = request.GET.get('teacher', '')
    if teacher_filter:
        schedules = schedules.filter(teacher__id=teacher_filter)

    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        schedules = schedules.filter(
            Q(subject__name__icontains=search_query) |
            Q(group__name__icontains=search_query) |
            Q(teacher__user__first_name__icontains=search_query) |
            Q(teacher__user__last_name__icontains=search_query)
        )

    paginator = Paginator(schedules, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Prepare weekly schedule for display
    weekly_schedule = {}
    if not group_filter and not teacher_filter:
        for schedule in schedules:
            day = schedule.day_of_week
            lesson = schedule.lesson_number
            if day not in weekly_schedule:
                weekly_schedule[day] = {}
            weekly_schedule[day][lesson] = schedule

    context = {
        'schedules': page_obj,
        'weekly_schedule': weekly_schedule,
        'total_count': schedules.count(),
        'group_filter': group_filter,
        'day_filter': day_filter,
        'teacher_filter': teacher_filter,
        'search_query': search_query,
        'groups': AcademicGroup.objects.filter(is_active=True),
        'teachers': Teacher.objects.filter(is_active=True),
        'days': Schedule.WEEKDAYS,
        'lesson_times': Schedule.LESSON_TIMES,
    }
    return render(request, 'schedule/list.html', context)


@login_required
def schedule_create(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        room_id = request.POST.get('room')
        day_of_week = request.POST.get('day_of_week')
        lesson_number = request.POST.get('lesson_number')
        lesson_type = request.POST.get('lesson_type')
        week_type = request.POST.get('week_type')
        subgroup = request.POST.get('subgroup', 1)
        academic_year = request.POST.get('academic_year')
        semester = request.POST.get('semester')

        if not all([group_id, subject_id, teacher_id, room_id, day_of_week, lesson_number, lesson_type, academic_year,
                    semester]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'schedule/form.html', {
                'title': "Dars qo'shish",
                'groups': AcademicGroup.objects.filter(is_active=True),
                'subjects': Subject.objects.all(),
                'teachers': Teacher.objects.filter(is_active=True),
                'rooms': Room.objects.filter(is_available=True),
                'days': Schedule.WEEKDAYS,
                'lesson_times': Schedule.LESSON_TIMES,
                'lesson_types': Schedule.LESSON_TYPES,
                'week_types': Schedule.WEEK_TYPES,
            })

        # Check for conflicts
        conflict = Schedule.objects.filter(
            group_id=group_id,
            day_of_week=day_of_week,
            lesson_number=lesson_number,
            week_type=week_type
        ).exists()

        if conflict:
            messages.error(request, "Bu vaqtga dars allaqachon qo'yilgan!")
            return render(request, 'schedule/form.html', {
                'title': "Dars qo'shish",
                'groups': AcademicGroup.objects.filter(is_active=True),
                'subjects': Subject.objects.all(),
                'teachers': Teacher.objects.filter(is_active=True),
                'rooms': Room.objects.filter(is_available=True),
                'days': Schedule.WEEKDAYS,
                'lesson_times': Schedule.LESSON_TIMES,
                'lesson_types': Schedule.LESSON_TYPES,
                'week_types': Schedule.WEEK_TYPES,
            })

        schedule = Schedule.objects.create(
            group_id=group_id,
            subject_id=subject_id,
            teacher_id=teacher_id,
            room_id=room_id,
            day_of_week=day_of_week,
            lesson_number=lesson_number,
            lesson_type=lesson_type,
            week_type=week_type,
            subgroup=subgroup,
            academic_year=academic_year,
            semester=semester
        )
        messages.success(request, f"Dars muvaffaqiyatli qo'shildi!")
        return redirect('schedule_list')

    context = {
        'title': "Dars qo'shish",
        'groups': AcademicGroup.objects.filter(is_active=True),
        'subjects': Subject.objects.all(),
        'teachers': Teacher.objects.filter(is_active=True),
        'rooms': Room.objects.filter(is_available=True),
        'days': Schedule.WEEKDAYS,
        'lesson_times': Schedule.LESSON_TIMES,
        'lesson_types': Schedule.LESSON_TYPES,
        'week_types': Schedule.WEEK_TYPES,
    }
    return render(request, 'schedule/form.html', context)


@login_required
def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)

    if request.method == 'POST':
        schedule.group_id = request.POST.get('group')
        schedule.subject_id = request.POST.get('subject')
        schedule.teacher_id = request.POST.get('teacher')
        schedule.room_id = request.POST.get('room')
        schedule.day_of_week = request.POST.get('day_of_week')
        schedule.lesson_number = request.POST.get('lesson_number')
        schedule.lesson_type = request.POST.get('lesson_type')
        schedule.week_type = request.POST.get('week_type')
        schedule.subgroup = request.POST.get('subgroup', 1)
        schedule.academic_year = request.POST.get('academic_year')
        schedule.semester = request.POST.get('semester')
        schedule.save()

        messages.success(request, f"Dars muvaffaqiyatli tahrirlandi!")
        return redirect('schedule_list')

    context = {
        'schedule': schedule,
        'title': "Dars tahrirlash",
        'groups': AcademicGroup.objects.filter(is_active=True),
        'subjects': Subject.objects.all(),
        'teachers': Teacher.objects.filter(is_active=True),
        'rooms': Room.objects.filter(is_available=True),
        'days': Schedule.WEEKDAYS,
        'lesson_times': Schedule.LESSON_TIMES,
        'lesson_types': Schedule.LESSON_TYPES,
        'week_types': Schedule.WEEK_TYPES,
    }
    return render(request, 'schedule/form.html', context)


@login_required
def schedule_delete(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, "Dars o'chirildi!")
        return redirect('schedule_list')
    return render(request, 'schedule/delete.html', {'schedule': schedule})


@login_required
def schedule_detail(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    return render(request, 'schedule/detail.html', {'schedule': schedule})


@login_required
def schedule_group_view(request, group_id):
    group = get_object_or_404(AcademicGroup, pk=group_id)
    schedules = Schedule.objects.filter(group=group).select_related('subject', 'teacher', 'room')

    # Create weekly schedule matrix
    weekly_matrix = {}
    for day in range(1, 7):
        weekly_matrix[day] = {}
        for lesson in range(1, 8):
            weekly_matrix[day][lesson] = None

    for s in schedules:
        weekly_matrix[s.day_of_week][s.lesson_number] = s

    context = {
        'group': group,
        'weekly_matrix': weekly_matrix,
        'days': Schedule.WEEKDAYS,
        'lesson_times': Schedule.LESSON_TIMES,
    }
    return render(request, 'schedule/group_schedule.html', context)


@login_required
def schedule_teacher_view(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    schedules = Schedule.objects.filter(teacher=teacher).select_related('group', 'subject', 'room')

    context = {
        'teacher': teacher,
        'schedules': schedules,
        'days': Schedule.WEEKDAYS,
    }
    return render(request, 'schedule/teacher_schedule.html', context)