from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import CarModel, Car, Order, OrderLine, Service
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    num_services = Service.objects.count()
    num_status = Order.objects.filter(status__exact='a').count()
    num_cars = Car.objects.count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_services': num_services,
        'num_status': num_status,
        'num_cars': num_cars,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def cars(request):
    paginator = Paginator(Car.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_cars = paginator.get_page(page_number)
    context = {
        'cars': paged_cars
    }
    return render(request, 'cars.html', context=context)


def car(request, car_id):
    single_car = get_object_or_404(Car, pk=car_id)
    return render(request, 'car.html', {'car': single_car})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 2
    template_name = 'order_list.html'


class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'order_detail.html'


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(owner__icontains=query) | Q(car_model__make__icontains=query) | Q(licence_plate__icontains=query) | Q(
            vin_code__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).filter(status__exact='v').order_by('due_back')
