from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from rgb_car_management.web.forms import CreateCarForm, EditCarForm, CreateCustomerForm, EditCustomerForm, \
    CreateIssuedCarForm, EditIssuedCarForm, LoginUserForm, RegisterUserForm, AcceptedCarForm
from rgb_car_management.web.mixins import SearchMixin, StaffOnlyMixin
from rgb_car_management.web.models import Customer, Car, IssuedCar, AcceptedCar, Employee


class HomeRedirect(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accepted cars')
        else:
            return redirect('login')


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
        return redirect('login')


class AcceptedCars(LoginRequiredMixin, SearchMixin, ListView):
    model = AcceptedCar
    template_name = 'accеpted_cars.html'
    context_object_name = 'accepted_cars'
    paginate_by = 10

    search_fields = [
        'car__registration_number'
    ]


class IssuedCars(LoginRequiredMixin, SearchMixin, ListView):
    model = IssuedCar
    template_name = 'issued_cars.html'
    context_object_name = 'issued_cars'
    paginate_by = 10

    search_fields = [
        'accepted_car__car__registration_number'
    ]


class Cars(LoginRequiredMixin, SearchMixin, ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    paginate_by = 10

    search_fields = [
        'registration_number'
    ]



class Customers(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    context_object_name = 'customers'
    paginate_by = 10


class CreateAcceptedCar(LoginRequiredMixin, CreateView):
    model = AcceptedCar
    template_name = 'accepted_car_actions.html'
    success_url = reverse_lazy('accepted cars')
    form_class = AcceptedCarForm


class EditAcceptedCar(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = AcceptedCar
    template_name = 'accepted_car_actions.html'
    success_url = reverse_lazy('accepted cars')
    form_class = AcceptedCarForm


class DeleteAcceptedCar(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        accepted_car = get_object_or_404(AcceptedCar, pk=pk)
        accepted_car.delete()

        return redirect('accepted cars')


class CreateIssuedCar(LoginRequiredMixin, CreateView):
    model = IssuedCar
    template_name = 'create_issued_car.html'
    success_url = reverse_lazy('issued cars')
    form_class = CreateIssuedCarForm


class EditIssuedCar(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = IssuedCar
    template_name = 'edit_issued_car.html'
    success_url = reverse_lazy('issued cars')
    form_class = EditIssuedCarForm


class DeleteIssuedCar(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        issued_car = get_object_or_404(IssuedCar, pk=pk)
        issued_car.delete()

        return redirect('issued cars')


class CreateCar(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'create_car.html'
    success_url = reverse_lazy('car_examination')
    form_class = CreateCarForm


class EditCar(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    model = Car
    template_name = 'edit_car.html'
    success_url = reverse_lazy('car_examination')
    form_class = EditCarForm


class DeleteCar(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()

        return redirect('car_examinations')


class CreateCustomer(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'create_customer.html'
    success_url = reverse_lazy('car_examination')
    form_class = CreateCustomerForm


class EditCustomer(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Customer
    template_name = 'edit_customer.html'
    success_url = reverse_lazy('car_examination')
    form_class = EditCustomerForm


class DeleteCustomer(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()

        return redirect('car_examinations')
