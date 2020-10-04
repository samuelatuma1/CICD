

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    context = {
        'flights': Flight.objects.all()
    }
    return render(request, 'flights/index.html', context)

def flight(request, flight_id):
    try:
        #pk means primary key
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist")

    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passenger":Passenger.objects.exclude(flights=flight).all()
    }

    return render(request, 'flights/flight.html', context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST['passenger'])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)

    except Passenger.DoesNotExist:
        return HttpResponse('No passenger')
    except Flight.DoesNotExist:
        return HttpResponse('No Flight')
    except KeyError:
        return HttpResponse('No data')
    
    passenger.flights.add(flight)

    return HttpResponseRedirect(reverse('flight', args=(flight_id,)))
    



