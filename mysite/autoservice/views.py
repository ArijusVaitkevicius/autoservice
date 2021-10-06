from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service


def index(request):
    num_services = Service.objects.count()
    num_status = Order.objects.filter(status__exact='a').count()
    num_cars = Car.objects.count()

    context = {
        'num_services': num_services,
        'num_status': num_status,
        'num_cars': num_cars,
    }

    return render(request, 'index.html', context=context)
