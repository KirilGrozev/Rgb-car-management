from django.urls import path

from rgb_car_management.web.views import CarExaminations, ReadyCars, Customers, CreateCarExamination, \
    EditCarExamination, DeleteCarExamination, CreateReadyCar, EditReadyCar, DeleteReadyCar, CreateCar, EditCar, \
    DeleteCar, CreateCustomer, EditCustomer, DeleteCustomer

urlpatterns = [
    path('car-examinations/', CarExaminations.as_view(), name='car examinations'),
    path('ready-car/', ReadyCars.as_view(), name='ready cars'),
    path('customers/', Customers.as_view(), name='customers'),
    path('create/car-examination/', CreateCarExamination.as_view(), name='create car examination'),
    path('edit/car-examination/<int:pk>/', EditCarExamination.as_view(), name='edit car examination'),
    path('delete/car-examination/<int:pk>/', DeleteCarExamination.as_view(), name='delete car examination'),
    path('create/ready-car/', CreateReadyCar.as_view(), name='create ready car'),
    path('edit/ready-car/<int:pk>/', EditReadyCar.as_view(), name='edit ready car'),
    path('delete/ready-car/<int:pk>/', DeleteReadyCar.as_view(), name='delete ready car'),
    path('create/car/', CreateCar.as_view(), name='create car'),
    path('edit/car/<int:pk>/', EditCar.as_view(), name='edit car'),
    path('delete/car/<int:pk>/', DeleteCar.as_view(), name='delete car'),
    path('create/customer/', CreateCustomer.as_view(), name='create customer'),
    path('edit/customer/<int:pk>/', EditCustomer.as_view(), name='edit customer'),
    path('delete/customer/<int:pk>/', DeleteCustomer.as_view(), name='delete customer'),
]