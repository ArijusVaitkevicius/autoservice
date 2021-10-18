from django.urls import path, include
from . import views

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', views.index, name='index'),
    path('cars/', views.cars, name='cars'),
    path('cars/<int:car_id>', views.car, name='car'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('myorders/', views.OrdersByUserListView.as_view(), name='my-orders'),
    path('myorders/new', views.OrderByUserCreateView.as_view(), name='new-order'),
    path('myorders/<int:pk>/update', views.OrderByUserUpdateView.as_view(), name='my-order-update'),
    path('myorders/<int:pk>/delete', views.OrderByUserDeleteView.as_view(), name='my-order-delete'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]
