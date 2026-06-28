from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles import finders
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from weasyprint import HTML, CSS

from rgb_car_management.web.forms import CreateCarForm, EditCarForm, CreateCustomerForm, EditCustomerForm, \
    LoginUserForm, RegisterUserForm
from rgb_car_management.web.mixins import SearchMixin, StaffOnlyMixin, AcceptedCarFormMixin, IssuedCarFormMixin
from rgb_car_management.web.models import Customer, Car, IssuedCar, AcceptedCar, Employee, CarProblem, CarIssue


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
    paginate_by = 25
    ordering = '-date'

    search_fields = [
        'car__registration_number'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_for_issuing'] = AcceptedCar.objects.filter(issuedcar__isnull=True).order_by('date')[:15]

        return context



class IssuedCars(LoginRequiredMixin, SearchMixin, ListView):
    model = IssuedCar
    template_name = 'issued_cars.html'
    context_object_name = 'issued_cars'
    paginate_by = 25
    ordering = '-date'

    search_fields = [
        'accepted_car__car__registration_number'
    ]


class Cars(LoginRequiredMixin, SearchMixin, ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'
    paginate_by = 25

    search_fields = [
        'registration_number'
    ]


class Customers(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers.html'
    context_object_name = 'customers'
    paginate_by = 25


class ProblemsJsonView(View):
    def get(self, request):
        items = CarProblem.objects.filter(category_id=request.GET.get('category')).values('id', 'name')
        return JsonResponse({'problems': list(items)})


class AcceptedIssuesJsonView(View):
    def get(self, request):
        car = get_object_or_404(AcceptedCar, pk=request.GET.get('accepted'))
        data = [
            {'category': i.category.id, 'problem': i.problem_id, 'other_issue': i.other_issue, 'is_other': i.category.is_other}
            for i in car.issues.select_related('category', 'problem')]
        return JsonResponse({'issues': data})


class CreateAcceptedCar(LoginRequiredMixin, AcceptedCarFormMixin, CreateView):
    pass


class AcceptedCarDetails(LoginRequiredMixin, DetailView):
    queryset = AcceptedCar.objects.select_related('car', 'customer', 'accepting_employee').prefetch_related('issues')
    template_name = 'accepted_car_details.html'


class EditAcceptedCar(LoginRequiredMixin, AcceptedCarFormMixin, StaffOnlyMixin, UpdateView):
    pass

class DeleteAcceptedCar(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        accepted_car = get_object_or_404(AcceptedCar, pk=pk)
        if hasattr(accepted_car, 'issuedcar'):
            messages.error(request, 'Не можеш да изтриеш вече издадена кола!')
            return redirect('accepted cars')

        accepted_car.issues.all().delete()
        accepted_car.delete()

        return redirect('accepted cars')


class CreateIssuedCar(LoginRequiredMixin, IssuedCarFormMixin, CreateView):
    pass


class IssuedCarDetails(LoginRequiredMixin, DetailView):
    queryset = IssuedCar.objects.select_related('accepted_car', 'mechanic').prefetch_related('repairs')
    template_name = 'issued_car_details.html'


class EditIssuedCar(LoginRequiredMixin, StaffOnlyMixin, IssuedCarFormMixin, UpdateView):
    pass


class DeleteIssuedCar(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        issued_car = get_object_or_404(IssuedCar, pk=pk)
        issued_car.repairs.all().delete()
        issued_car.delete()

        return redirect('issued cars')


class CreateCar(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'create_car.html'
    success_url = reverse_lazy('accepted cars')
    form_class = CreateCarForm


class EditCar(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Car
    template_name = 'edit_car.html'
    success_url = reverse_lazy('accepted cars')
    form_class = EditCarForm


class DeleteCar(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()

        return redirect('accepted cars')


class CreateCustomer(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'create_customer.html'
    success_url = reverse_lazy('accepted cars')
    form_class = CreateCustomerForm


class EditCustomer(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Customer
    template_name = 'edit_customer.html'
    success_url = reverse_lazy('accepted cars')
    form_class = EditCustomerForm


class DeleteCustomer(LoginRequiredMixin, StaffOnlyMixin, View):
    def post(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()

        return redirect('accepted cars')


class AcceptedCarPdf(View):
    def get(self, request, pk):
        obj = get_object_or_404(AcceptedCar, pk=pk)

        html_string = render_to_string(
            "documents/accepted_car_pdf.html",
            {'object': obj},
            request=request,
        )
        css_path = finders.find('css/document_css.css')

        pdf_bytes = HTML(
            string=html_string,
            base_url=request.build_absolute_uri('/'),
        ).write_pdf(stylesheets=[CSS(filename=css_path)])

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="priem-{obj.pk:04d}.pdf"'
        return response


class IssuedCarPdf(View):
    def get(self, request, pk):
        obj = get_object_or_404(IssuedCar, pk=pk)

        html_string = render_to_string(
            "documents/issued_car_pdf.html",
            {'object': obj},
            request=request,
        )
        css_path = finders.find('css/document_css.css')

        pdf_bytes = HTML(
            string=html_string,
            base_url=request.build_absolute_uri('/'),
        ).write_pdf(stylesheets=[CSS(filename=css_path)])

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="izdavane-{obj.pk:04d}.pdf"'
        return response
