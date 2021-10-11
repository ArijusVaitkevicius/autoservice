from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField


class CarModel(models.Model):
    make = models.CharField('Make', max_length=200)
    model = models.CharField('Model', max_length=200)

    def __str__(self):
        return f'{self.make} {self.model}'

    class Meta:
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'


class Car(models.Model):
    licence_plate = models.CharField('Licence plate', max_length=200)
    car_model = models.ForeignKey('CarModel', on_delete=models.SET_NULL, null=True)
    vin_code = models.CharField('VIN code', max_length=200)
    owner = models.CharField('Owner', max_length=200, null=True)
    year = models.IntegerField(null=True)
    cover = models.ImageField('Cover', upload_to='covers', null=True)
    description = HTMLField('Description', null=True)

    def __str__(self):
        return f"{self.owner}: {self.car_model}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'


class Order(models.Model):
    date = models.DateField('Date', null=True, blank=True)
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField('Back_date', null=True, blank=True)

    ORDER_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atlikta'),
        ('t', 'Atšaukta'),
    )

    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='p',
        help_text='Status',
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def count_amount(self):
        return 0

    count_amount.short_description = 'Amount'

    def __str__(self):
        return f'{self.date} {self.car}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, related_name='lines')
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField('Quantity')

    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"

    class Meta:
        verbose_name = 'Order Line'
        verbose_name_plural = 'Order Lines'


class Service(models.Model):
    name = models.CharField('Name', max_length=200)
    price = models.FloatField('Price Eur.')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
