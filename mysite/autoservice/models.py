from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


class CarModel(models.Model):
    make = models.CharField(_('Make'), max_length=200)
    model = models.CharField(_('Model'), max_length=200)

    def __str__(self):
        return f'{self.make} {self.model}'

    class Meta:
        verbose_name = _('Car Model')
        verbose_name_plural = _('Car Models')


class Car(models.Model):
    licence_plate = models.CharField(_('Licence plate'), max_length=200)
    car_model = models.ForeignKey('CarModel', on_delete=models.SET_NULL, null=True)
    vin_code = models.CharField(_('VIN code'), max_length=200)
    owner = models.CharField(_('Owner'), max_length=200, null=True)
    year = models.IntegerField(_('Year'), null=True)
    cover = models.ImageField(_('Cover'), upload_to='covers', null=True)
    description = HTMLField(_('Description'), blank=True, null=True)

    def __str__(self):
        return f"{self.owner}: {self.car_model}, {self.licence_plate}, {self.vin_code}"

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    car = models.ForeignKey('Car', on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_back = models.DateField(_('Back_date'), null=True, blank=True)

    ORDER_STATUS = (
        ('p', _('Confirmed')),
        ('v', _('In progress')),
        ('a', _('Done')),
        ('t', _('Canceled')),
    )

    status = models.CharField(
        max_length=1,
        choices=ORDER_STATUS,
        blank=True,
        default='p',
        help_text=_('Status'),
    )

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    @property
    def total(self):
        order_lines = OrderLine.objects.filter(order=self.id)
        total = 0
        for line in order_lines:
            total += line.service.price * line.qty
        return total

    def __str__(self):
        return f'{self.date} {self.car}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=200)
    price = models.FloatField(_('Price Eur.'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class OrderLine(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, related_name='lines')
    service = models.ForeignKey('Service', on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(_('Quantity'))

    @property
    def line_total(self):
        return self.service.price * self.qty

    def __str__(self):
        return f"{self.order}: {self.service}, {self.qty}"

    class Meta:
        verbose_name = _('Order Line')
        verbose_name_plural = _('Order Lines')


class OrderComment(models.Model):
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='comments')
    commentator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField(_('Comment'), max_length=2000)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.png", upload_to="profile_pics")

    def __str__(self):
        return _(f"{self.user.username} profile")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 200 or img.width > 200:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.photo.path)
