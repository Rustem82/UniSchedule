from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum  # Импортируем Sum
from .models import Building, Room


# Building Views
@login_required
def building_list(request):
    buildings = Building.objects.all().annotate(rooms_count=Count('rooms'))

    search_query = request.GET.get('search', '')
    if search_query:
        buildings = buildings.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(address__icontains=search_query)
        )

    paginator = Paginator(buildings, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'buildings': page_obj,
        'total_count': buildings.count(),
        'search_query': search_query,
    }
    return render(request, 'rooms/buildings/list.html', context)


@login_required
def building_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        address = request.POST.get('address')
        floors = request.POST.get('floors', 0)
        description = request.POST.get('description', '')

        if not all([name, code, address]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'rooms/buildings/form.html', {'title': "Bino qo'shish"})

        if Building.objects.filter(code=code).exists():
            messages.error(request, f"'{code}' kodi bilan bino allaqachon mavjud!")
            return render(request, 'rooms/buildings/form.html', {'title': "Bino qo'shish"})

        building = Building.objects.create(
            name=name, code=code, address=address,
            floors=floors, description=description
        )
        messages.success(request, f"'{building.name}' binosi muvaffaqiyatli qo'shildi!")
        return redirect('building_list')

    return render(request, 'rooms/buildings/form.html', {'title': "Bino qo'shish"})


@login_required
def building_edit(request, pk):
    building = get_object_or_404(Building, pk=pk)

    if request.method == 'POST':
        building.name = request.POST.get('name')
        building.code = request.POST.get('code')
        building.address = request.POST.get('address')
        building.floors = request.POST.get('floors', 0)
        building.description = request.POST.get('description', '')
        building.save()
        messages.success(request, f"'{building.name}' binosi tahrirlandi!")
        return redirect('building_list')

    return render(request, 'rooms/buildings/form.html', {'building': building, 'title': "Bino tahrirlash"})


@login_required
def building_delete(request, pk):
    building = get_object_or_404(Building, pk=pk)
    if request.method == 'POST':
        building_name = building.name
        building.delete()
        messages.success(request, f"'{building_name}' binosi o'chirildi!")
        return redirect('building_list')
    return render(request, 'rooms/buildings/delete.html', {'building': building})


@login_required
def building_detail(request, pk):
    building = get_object_or_404(Building, pk=pk)
    rooms = building.rooms.all()

    context = {
        'building': building,
        'rooms': rooms,
        'total_rooms': rooms.count(),
    }
    return render(request, 'rooms/buildings/detail.html', context)


# Room Views
@login_required
def room_list(request):
    rooms = Room.objects.all().select_related('building')

    search_query = request.GET.get('search', '')
    if search_query:
        rooms = rooms.filter(
            Q(number__icontains=search_query) |
            Q(building__name__icontains=search_query) |
            Q(building__code__icontains=search_query)
        )

    building_filter = request.GET.get('building', '')
    if building_filter:
        rooms = rooms.filter(building__id=building_filter)

    room_type_filter = request.GET.get('room_type', '')
    if room_type_filter:
        rooms = rooms.filter(room_type=room_type_filter)

    paginator = Paginator(rooms, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Исправлено: используем Sum вместо models.Sum
    total_capacity = rooms.aggregate(total=Sum('capacity'))['total'] or 0

    context = {
        'rooms': page_obj,
        'total_count': rooms.count(),
        'total_capacity': total_capacity,
        'search_query': search_query,
        'building_filter': building_filter,
        'room_type_filter': room_type_filter,
        'buildings': Building.objects.all(),
        'room_types': Room.ROOM_TYPES,
    }
    return render(request, 'rooms/rooms/list.html', context)


@login_required
def room_create(request):
    if request.method == 'POST':
        building_id = request.POST.get('building')
        number = request.POST.get('number')
        capacity = request.POST.get('capacity', 0)
        room_type = request.POST.get('room_type')
        floor = request.POST.get('floor', 1)
        has_projector = request.POST.get('has_projector') == 'on'
        has_computer = request.POST.get('has_computer') == 'on'
        has_whiteboard = request.POST.get('has_whiteboard') == 'on'
        has_air_conditioner = request.POST.get('has_air_conditioner') == 'on'
        has_wifi = request.POST.get('has_wifi') == 'on'
        is_available = request.POST.get('is_available') == 'on'
        description = request.POST.get('description', '')

        if not all([building_id, number, room_type]):
            messages.error(request, "Iltimos, barcha majburiy maydonlarni to'ldiring!")
            return render(request, 'rooms/rooms/form.html', {
                'title': "Xona qo'shish",
                'buildings': Building.objects.all(),
                'room_types': Room.ROOM_TYPES,
            })

        building = get_object_or_404(Building, id=building_id)

        if Room.objects.filter(building=building, number=number).exists():
            messages.error(request, f"{building.name} binosida {number} xonasi allaqachon mavjud!")
            return render(request, 'rooms/rooms/form.html', {
                'title': "Xona qo'shish",
                'buildings': Building.objects.all(),
                'room_types': Room.ROOM_TYPES,
            })

        room = Room.objects.create(
            building=building, number=number, capacity=capacity, room_type=room_type,
            floor=floor, has_projector=has_projector, has_computer=has_computer,
            has_whiteboard=has_whiteboard, has_air_conditioner=has_air_conditioner,
            has_wifi=has_wifi, is_available=is_available, description=description
        )
        messages.success(request, f"'{room}' xonasi qo'shildi!")
        return redirect('room_list')

    context = {
        'title': "Xona qo'shish",
        'buildings': Building.objects.all(),
        'room_types': Room.ROOM_TYPES,
    }
    return render(request, 'rooms/rooms/form.html', context)


@login_required
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)

    if request.method == 'POST':
        building_id = request.POST.get('building')
        room.number = request.POST.get('number')
        room.capacity = request.POST.get('capacity', 0)
        room.room_type = request.POST.get('room_type')
        room.floor = request.POST.get('floor', 1)
        room.has_projector = request.POST.get('has_projector') == 'on'
        room.has_computer = request.POST.get('has_computer') == 'on'
        room.has_whiteboard = request.POST.get('has_whiteboard') == 'on'
        room.has_air_conditioner = request.POST.get('has_air_conditioner') == 'on'
        room.has_wifi = request.POST.get('has_wifi') == 'on'
        room.is_available = request.POST.get('is_available') == 'on'
        room.description = request.POST.get('description', '')

        if building_id:
            room.building = get_object_or_404(Building, id=building_id)

        room.save()
        messages.success(request, f"'{room}' xonasi tahrirlandi!")
        return redirect('room_list')

    context = {
        'room': room,
        'title': "Xona tahrirlash",
        'buildings': Building.objects.all(),
        'room_types': Room.ROOM_TYPES,
    }
    return render(request, 'rooms/rooms/form.html', context)


@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_name = str(room)
        room.delete()
        messages.success(request, f"'{room_name}' xonasi o'chirildi!")
        return redirect('room_list')
    return render(request, 'rooms/rooms/delete.html', {'room': room})


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/rooms/detail.html', {'room': room})