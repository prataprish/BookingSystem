from django.shortcuts import render
from django.http import Http404, HttpResponse
from .models import Screen # reference to models in models.py
from django.views.decorators.csrf import csrf_exempt
import json
import re

# @csrf_exempt used for bypassing crsf required by Django, should be removed while used at production for security
@csrf_exempt
def index(request):

    if request.method == 'POST':
        screen = json.loads(request.POST['data']) #POST data
        new_screen = screen['name']
        row_names = screen['seatInfo'].keys()
        for row_name in row_names:
            aisleSeats = screen['seatInfo'][row_name]['aisleSeats']
            numberOfSeats = screen['seatInfo'][row_name]['numberOfSeats']
            seats_available = screen['seatInfo'][row_name]['aisleSeats']
            new_row = Screen(row=row_name,screen=new_screen,number_of_seats=numberOfSeats,aisle_seats=json.dumps(seats_available),seats_unavailable=json.dumps([])) # call to class Screen in models.py
            new_row.save()
        return HttpResponse('Saved')


@csrf_exempt
def reserve(request,screen):
    if request.method == 'POST':
        seats = json.loads(request.POST['seats'])
        if Screen.objects.book(screen,seats): # method defined as book() under class ScreenManager in models.py
            return HttpResponse(status=200) # reserve successful
        else:
            return HttpResponse(status=400) # reserve unsuccessful

def available(request,screen):
    if request.method == 'GET':
        if 'status' in request.GET:
            if request.GET['status'] == 'unreserved':
                result = Screen.objects.allAvailable(screen) # list of unreserved seats, method defined as allAvailable() under class ScreenManager in models.py
                return HttpResponse(result)
        elif 'numSeats' in request.GET and 'choice' in request.GET:
            choice = request.GET['choice']
            choice = re.match(r"(?P<row>[a-zA-Z]+)(?P<seat>.+)$",choice) # grouping seat number and rows
            available = Screen.objects.returnContigous(screen,{'row':choice.group('row'),'seat':int(choice.group('seat'))},request.GET['numSeats']) # method defined as returnContigous() under class ScreenManager in models.py
            return HttpResponse(available)
