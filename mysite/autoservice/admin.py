from django.contrib import admin
from .models import CarModel, Car, Order, OrderLine, Service, OrderComment, Profile


# Register your models here.

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0  # išjungia placeholder'ius


class OrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'client', 'due_back')
    inlines = [OrderLineInline]


class CarAdmin(admin.ModelAdmin):
    list_display = ('owner', 'car_model', 'licence_plate', 'vin_code')
    list_filter = ('owner', 'car_model')
    search_fields = ('licence_plate', 'vin_code')


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


class OrderCommentAdmin(admin.ModelAdmin):
    list_display = ('order', 'commentator', 'date_created', 'content')


admin.site.register(CarModel)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(Service, ServiceAdmin)
admin.site.register(OrderComment, OrderCommentAdmin)
admin.site.register(Profile)
