from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Teacher
from departments.models import Department


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all().select_related('user', 'department')

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(department__name__icontains=search_query)
        )

    # Filter by department
    department_filter = request.GET.get('department', '')
    if department_filter:
        teachers = teachers.filter(department__id=department_filter)

    # Filter by position
    position_filter = request.GET.get('position', '')
    if position_filter:
        teachers = teachers.filter(position=position_filter)

    # Filter by academic degree
    degree_filter = request.GET.get('degree', '')
    if degree_filter:
        teachers = teachers.filter(academic_degree=degree_filter)

    # Filter by active status
    active_filter = request.GET.get('active', '')
    if active_filter:
        teachers = teachers.filter(is_active=active_filter == 'true')

    # Pagination
    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'teachers': page_obj,
        'total_count': teachers.count(),
        'search_query': search_query,
        'department_filter': department_filter,
        'position_filter': position_filter,
        'degree_filter': degree_filter,
        'active_filter': active_filter,
        'departments': Department.objects.all(),
        'positions': Teacher.POSITIONS,
        'academic_degrees': Teacher.ACADEMIC_DEGREES,
    }
    return render(request, 'teachers/list.html', context)


@login_required
def teacher_create(request):
    if request.method == 'POST':
        # User data
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Teacher data
        department_id = request.POST.get('department')
        employee_id = request.POST.get('employee_id')
        position = request.POST.get('position')
        academic_degree = request.POST.get('academic_degree')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        birth_date = request.POST.get('birth_date')
        start_date = request.POST.get('start_date')
        is_active = request.POST.get('is_active') == 'on'

        # Validation
        if not all([username, first_name, last_name, password, department_id, position]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'teachers/form.html', {
                'title': "O'qituvchi qo'shish",
                'departments': Department.objects.all(),
                'positions': Teacher.POSITIONS,
                'academic_degrees': Teacher.ACADEMIC_DEGREES,
            })

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, f"'{username}' username allaqachon mavjud!")
            return render(request, 'teachers/form.html', {
                'title': "O'qituvchi qo'shish",
                'departments': Department.objects.all(),
                'positions': Teacher.POSITIONS,
                'academic_degrees': Teacher.ACADEMIC_DEGREES,
            })

        # Check if employee_id exists
        if employee_id and Teacher.objects.filter(employee_id=employee_id).exists():
            messages.error(request, f"'{employee_id}' xodim ID allaqachon mavjud!")
            return render(request, 'teachers/form.html', {
                'title': "O'qituvchi qo'shish",
                'departments': Department.objects.all(),
                'positions': Teacher.POSITIONS,
                'academic_degrees': Teacher.ACADEMIC_DEGREES,
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create teacher
        department = get_object_or_404(Department, id=department_id)
        teacher = Teacher.objects.create(
            user=user,
            department=department,
            employee_id=employee_id,
            position=position,
            academic_degree=academic_degree,
            phone=phone,
            address=address,
            birth_date=birth_date if birth_date else None,
            start_date=start_date if start_date else None,
            is_active=is_active
        )

        messages.success(request, f"'{teacher.get_full_name()}' o'qituvchisi muvaffaqiyatli qo'shildi!")
        return redirect('teacher_list')

    context = {
        'title': "O'qituvchi qo'shish",
        'departments': Department.objects.all(),
        'positions': Teacher.POSITIONS,
        'academic_degrees': Teacher.ACADEMIC_DEGREES,
    }
    return render(request, 'teachers/form.html', context)


@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        # User data
        teacher.user.first_name = request.POST.get('first_name')
        teacher.user.last_name = request.POST.get('last_name')
        teacher.user.email = request.POST.get('email')

        # Teacher data
        department_id = request.POST.get('department')
        teacher.employee_id = request.POST.get('employee_id')
        teacher.position = request.POST.get('position')
        teacher.academic_degree = request.POST.get('academic_degree')
        teacher.phone = request.POST.get('phone')
        teacher.address = request.POST.get('address')
        teacher.birth_date = request.POST.get('birth_date') or None
        teacher.start_date = request.POST.get('start_date') or None
        teacher.is_active = request.POST.get('is_active') == 'on'

        if department_id:
            teacher.department = get_object_or_404(Department, id=department_id)

        teacher.user.save()
        teacher.save()

        messages.success(request, f"'{teacher.get_full_name()}' o'qituvchisi muvaffaqiyatli tahrirlandi!")
        return redirect('teacher_list')

    context = {
        'teacher': teacher,
        'title': "O'qituvchi tahrirlash",
        'departments': Department.objects.all(),
        'positions': Teacher.POSITIONS,
        'academic_degrees': Teacher.ACADEMIC_DEGREES,
    }
    return render(request, 'teachers/form.html', context)


@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        teacher_name = teacher.get_full_name()
        teacher.user.delete()  # This will delete the teacher too (CASCADE)
        messages.success(request, f"'{teacher_name}' o'qituvchisi o'chirildi!")
        return redirect('teacher_list')

    return render(request, 'teachers/delete.html', {'teacher': teacher})


@login_required
def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    context = {
        'teacher': teacher,
    }
    return render(request, 'teachers/detail.html', context)