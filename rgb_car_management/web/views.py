from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from rgb_car_management.web.forms import CreateCarExaminationForm, EditCarExaminationForm, CreateReadyCarForm, \
    EditReadyCarForm, CreateCarForm, EditCarForm, CreateCustomerForm, EditCustomerForm
from rgb_car_management.web.models import CarExamination, CarReady, Customer, Car


class CarExaminations(ListView):
    model = CarExamination
    template_name = 'car_examinations.html'


class ReadyCars(ListView):
    model = CarReady
    template_name = 'ready_cars.html'


class Customers(ListView):
    model = Customer
    template_name = 'customers.html'


class CreateCarExamination(CreateView):
    model = CarExamination
    template_name = 'create_car_examination.html'
    success_url = redirect('car_examinations')
    form_class = CreateCarExaminationForm


class EditCarExamination(UpdateView):
    model = CarExamination
    template_name = 'edit_car_examination.html'
    success_url = redirect('car_examinations')
    form_class = EditCarExaminationForm


class DeleteCarExamination(View):
    def post(self, request, pk):
        car_examination = get_object_or_404(CarExamination, pk=pk)
        car_examination.delete()

        return redirect('car_examinations')


class CreateReadyCar(CreateView):
    model = CarReady
    template_name = 'create_ready_car.html'
    success_url = redirect('ready_car')
    form_class = CreateReadyCarForm


class EditReadyCar(UpdateView):
    model = CarReady
    template_name = 'edit_ready_car.html'
    success_url = redirect('ready_car')
    form_class = EditReadyCarForm


class DeleteReadyCar(View):
    def post(self, request, pk):
        ready_car = get_object_or_404(CarReady, pk=pk)
        ready_car.delete()

        return redirect('ready_cars')


class CreateCar(CreateView):
    model = Car
    template_name = 'create_car.html'
    success_url = redirect('car_examination')
    form_class = CreateCarForm


class EditCar(CreateView):
    model = Car
    template_name = 'edit_car.html'
    success_url = redirect('car_examination')
    form_class = EditCarForm


class DeleteCar(View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()

        return redirect('car_examinations')


class CreateCustomer(CreateView):
    model = Customer
    template_name = 'create_customer.html'
    success_url = redirect('car_examination')
    form_class = CreateCustomerForm


class EditCustomer(UpdateView):
    model = Customer
    template_name = 'edit_customer.html'
    success_url = redirect('car_examination')
    form_class = EditCustomerForm


class DeleteCustomer(View):
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()

        return redirect('car_examinations')
