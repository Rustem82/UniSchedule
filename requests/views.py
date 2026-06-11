from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import WorkloadRequest
from departments.models import Department
from subjects.models import Subject
from teachers.models import Teacher


@login_required
def request_list(request):
    # Get current user's department (assuming teacher has department)
    user_teacher = Teacher.objects.filter(user=request.user).first()

    # Get requests based on tab
    tab = request.GET.get('tab', 'all')

    if tab == 'sent':
        requests_list = WorkloadRequest.objects.filter(
            from_department=user_teacher.department if user_teacher else None)
    elif tab == 'received':
        requests_list = WorkloadRequest.objects.filter(to_department=user_teacher.department if user_teacher else None)
    else:
        requests_list = WorkloadRequest.objects.all()

    requests_list = requests_list.select_related('from_department', 'to_department', 'subject', 'teacher', 'created_by')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        requests_list = requests_list.filter(
            Q(subject__name__icontains=search_query) |
            Q(from_department__name__icontains=search_query) |
            Q(to_department__name__icontains=search_query) |
            Q(message__icontains=search_query)
        )

    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        requests_list = requests_list.filter(status=status_filter)

    # Filter by request type
    type_filter = request.GET.get('type', '')
    if type_filter:
        requests_list = requests_list.filter(request_type=type_filter)

    # Pagination
    paginator = Paginator(requests_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Statistics
    stats = {
        'total': WorkloadRequest.objects.count(),
        'pending': WorkloadRequest.objects.filter(status='pending').count(),
        'approved': WorkloadRequest.objects.filter(status='approved').count(),
        'rejected': WorkloadRequest.objects.filter(status='rejected').count(),
        'sent': WorkloadRequest.objects.filter(
            from_department=user_teacher.department if user_teacher else None).count(),
        'received': WorkloadRequest.objects.filter(
            to_department=user_teacher.department if user_teacher else None).count(),
    }

    context = {
        'requests': page_obj,
        'total_count': requests_list.count(),
        'search_query': search_query,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'tab': tab,
        'stats': stats,
        'status_choices': WorkloadRequest.STATUS_CHOICES,
        'request_types': WorkloadRequest.REQUEST_TYPES,
        'departments': Department.objects.all(),
    }
    return render(request, 'requests/list.html', context)


@login_required
def request_create(request):
    user_teacher = Teacher.objects.filter(user=request.user).first()

    if request.method == 'POST':
        from_department_id = request.POST.get('from_department')
        to_department_id = request.POST.get('to_department')
        subject_id = request.POST.get('subject')
        teacher_id = request.POST.get('teacher')
        semester = request.POST.get('semester')
        total_hours = request.POST.get('total_hours', 0)
        lecture_hours = request.POST.get('lecture_hours', 0)
        practical_hours = request.POST.get('practical_hours', 0)
        lab_hours = request.POST.get('lab_hours', 0)
        message = request.POST.get('message', '')
        request_type = request.POST.get('request_type', 'standard')

        if not all([to_department_id, subject_id, semester, total_hours]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'requests/form.html', {
                'title': "Yangi talabnoma",
                'departments': Department.objects.all(),
                'subjects': Subject.objects.all(),
                'teachers': Teacher.objects.filter(is_active=True),
                'status_choices': WorkloadRequest.STATUS_CHOICES,
                'request_types': WorkloadRequest.REQUEST_TYPES,
            })

        workload_request = WorkloadRequest.objects.create(
            from_department_id=from_department_id or (user_teacher.department.id if user_teacher else None),
            to_department_id=to_department_id,
            subject_id=subject_id,
            teacher_id=teacher_id if teacher_id else None,
            semester=semester,
            total_hours=total_hours,
            lecture_hours=lecture_hours,
            practical_hours=practical_hours,
            lab_hours=lab_hours,
            message=message,
            request_type=request_type,
            status='sent' if request_type == 'urgent' else 'pending',
            created_by=user_teacher,
        )
        messages.success(request, f"Talabnoma #{workload_request.id} muvaffaqiyatli yuborildi!")
        return redirect('request_list')

    context = {
        'title': "Yangi talabnoma",
        'departments': Department.objects.all(),
        'subjects': Subject.objects.all(),
        'teachers': Teacher.objects.filter(is_active=True),
        'status_choices': WorkloadRequest.STATUS_CHOICES,
        'request_types': WorkloadRequest.REQUEST_TYPES,
        'user_teacher': user_teacher,
    }
    return render(request, 'requests/form.html', context)


@login_required
def request_detail(request, pk):
    req = get_object_or_404(WorkloadRequest, pk=pk)
    return render(request, 'requests/detail.html', {'request': req})


@login_required
def request_approve(request, pk):
    req = get_object_or_404(WorkloadRequest, pk=pk)
    user_teacher = Teacher.objects.filter(user=request.user).first()

    if request.method == 'POST':
        req.status = 'approved'
        req.approved_at = timezone.now()
        req.approved_by = user_teacher
        req.save()
        messages.success(request, f"Talabnoma #{req.id} tasdiqlandi!")
        return redirect('request_list')

    return render(request, 'requests/approve.html', {'request': req})


@login_required
def request_reject(request, pk):
    req = get_object_or_404(WorkloadRequest, pk=pk)
    user_teacher = Teacher.objects.filter(user=request.user).first()

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        req.status = 'rejected'
        req.rejection_reason = rejection_reason
        req.save()
        messages.warning(request, f"Talabnoma #{req.id} rad etildi!")
        return redirect('request_list')

    return render(request, 'requests/reject.html', {'request': req})


@login_required
def request_cancel(request, pk):
    req = get_object_or_404(WorkloadRequest, pk=pk)

    if request.method == 'POST':
        req.status = 'cancelled'
        req.save()
        messages.info(request, f"Talabnoma #{req.id} bekor qilindi!")
        return redirect('request_list')

    return render(request, 'requests/cancel.html', {'request': req})


@login_required
def request_delete(request, pk):
    req = get_object_or_404(WorkloadRequest, pk=pk)

    if request.method == 'POST':
        req_id = req.id
        req.delete()
        messages.success(request, f"Talabnoma #{req_id} o'chirildi!")
        return redirect('request_list')

    return render(request, 'requests/delete.html', {'request': req})