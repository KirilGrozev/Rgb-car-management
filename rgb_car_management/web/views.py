from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from rgb_car_management.web.forms import CreateCarForm, EditCarForm, CreateCustomerForm, EditCustomerForm, \
    CreateAcceptedCarForm, \
    EditAcceptedCarForm, CreateIssuedCarForm, EditIssuedCarForm, LoginUserForm, RegisterUserForm
from rgb_car_management.web.models import Customer, Car, IssuedCar, AcceptedCar, Employee


class Register(CreateView):
    model = Employee
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('accepted cars')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        return result


class Login(LoginView):
    model = Employee
    template_name = 'login.html'
    form_class = LoginUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('accepted cars')


class Logout(LoginRequiredMixin, LogoutView):
    def get(self, request):
        logout(request)
        return redirect('register')


class AcceptedCars(LoginRequiredMixin, ListView):
    model = AcceptedCar
    template_name = 'accеpted_cars.html'


class IssuedCars(LoginRequiredMixin, ListView):
    model = IssuedCar
    template_name = 'issued_cars.html'


class Cars(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars.html'


class Customers(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'


class CreateAcceptedCar(LoginRequiredMixin, CreateView):
    model = AcceptedCar
    template_name = 'create_accepted_car.html'
    success_url = reverse_lazy('accepted cars')
    form_class = CreateAcceptedCarForm


class EditAcceptedCar(LoginRequiredMixin, UpdateView):
    model = AcceptedCar
    template_name = 'edit_accepted_car.html'
    success_url = reverse_lazy('accepted cars')
    form_class = EditAcceptedCarForm


class DeleteAcceptedCar(LoginRequiredMixin, View):
    def post(self, request, pk):
        accepted_car = get_object_or_404(AcceptedCar, pk=pk)
        accepted_car.delete()

        return redirect('accepted cars')


class CreateIssuedCar(LoginRequiredMixin, CreateView):
    model = IssuedCar
    template_name = 'create_issued_car.html'
    success_url = reverse_lazy('issued cars')
    form_class = CreateIssuedCarForm


class EditIssuedCar(LoginRequiredMixin, UpdateView):
    model = IssuedCar
    template_name = 'edit_issued_car.html'
    success_url = reverse_lazy('issued cars')
    form_class = EditIssuedCarForm


class DeleteIssuedCar(LoginRequiredMixin, View):
    def post(self, request, pk):
        issued_car = get_object_or_404(IssuedCar, pk=pk)
        issued_car.delete()

        return redirect('issued cars')


class CreateCar(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'create_car.html'
    success_url = reverse_lazy('car_examination')
    form_class = CreateCarForm


class EditCar(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'edit_car.html'
    success_url = reverse_lazy('car_examination')
    form_class = EditCarForm


class DeleteCar(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()

        return redirect('car_examinations')


class CreateCustomer(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'create_customer.html'
    success_url = reverse_lazy('car_examination')
    form_class = CreateCustomerForm


class EditCustomer(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'edit_customer.html'
    success_url = reverse_lazy('car_examination')
    form_class = EditCustomerForm


class DeleteCustomer(LoginRequiredMixin, View):
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()

        return redirect('car_examinations')
