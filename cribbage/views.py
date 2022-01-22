from django.shortcuts import render


def index(request):
    return render(request, 'cribbage/index.html')

def room(request, room_name):
    return render(request, 'cribbage/room.html', {
        'room_name': room_name
    })