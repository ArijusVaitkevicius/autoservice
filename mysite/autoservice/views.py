from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service
from django.views import generic


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


def cars(request):
    all_cars = Car.objects.all()
    context = {
        'cars': all_cars
    }
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    template_name = 'order_list.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'
