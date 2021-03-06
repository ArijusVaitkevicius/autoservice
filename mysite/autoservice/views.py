from django.shortcuts import render, get_object_or_404, reverse
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from .models import CarModel, Car, Order, OrderLine, Service
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from inspect import currentframe


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
    template_name = 'orders.html'


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order.html'
    form_class = OrderCommentForm

    # class Meta:
    #     ordering = ['title']

    def get_success_url(self):
        return reverse('order-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, *args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['form'] = OrderCommentForm(initial={'order': self.object})
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.commentator = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'user_orders.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('due_back')


class OrderInline(InlineFormSetFactory):
    model = OrderLine
    fields = ['service', 'qty']


class OrderByUserCreateView(LoginRequiredMixin, CreateWithInlinesView):
    model = Order
    inlines = [OrderInline, ]
    fields = ['car', 'due_back']
    success_url = "/autoservice/orders/"
    template_name = 'order_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderByUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateWithInlinesView):
    model = Order
    inlines = [OrderInline, ]
    fields = ['car', 'due_back']
    success_url = "/autoservice/myorders/"
    template_name = 'order_form.html'

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.client


class OrderByUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    success_url = "/autoservice/myorders/"
    template_name = 'order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.client


def search(request):
    """
    paprasta paie??ka. query ima informacij?? i?? paie??kos laukelio,
    search_results prafiltruoja pagal ??vest?? tekst?? knyg?? pavadinimus ir apra??ymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raid??s
    did??iosios/ma??osios.
    """
    query = request.GET.get('query')
    search_results = Car.objects.filter(
        Q(owner__icontains=query) | Q(car_model__make__icontains=query) | Q(licence_plate__icontains=query) | Q(
            vin_code__icontains=query))
    return render(request, 'search.html', {'cars': search_results, 'query': query})


def f(s):
    frame = currentframe().f_back
    return eval(f"f'{s}'", frame.f_locals, frame.f_globals)

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reik??mes i?? registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slapta??od??iai
        if password == password2:
            # tikriname, ar neu??imtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f(_('Username {username} is already in use!')))
                return redirect('register')
            else:
                # tikriname, ar n??ra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f(_('Email {email} is already in use!')))
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame nauj?? vartotoj??
                    User.objects.create_user(username=username, email=email, password=password)
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)
