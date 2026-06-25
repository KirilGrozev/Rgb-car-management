from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.forms import Select
from django_select2 import forms as select2_forms
from django_select2.forms import ModelSelect2Widget
from libmambapy.bindings.solver import ProblemsGraph

from rgb_car_management.web.models import Car, Customer, AcceptedCar, IssuedCar, Employee, CarIssue, CarProblem


class RegisterUserForm(UserCreationForm):
    user = None

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('first_name', 'last_name', 'email')

        label = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'email': 'Имейл',
        }

    widgets = {
        'first_name': forms.TextInput(attrs={'placeholder': 'Въведи име'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Въведи фамилия'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Въведи имейл'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = Employee
        fields = '__all__'

        label = {
            'username': 'Имейл',
            'password': 'Парола'
        }

    widgets = {
        'username': forms.EmailInput(attrs={'placeholder': 'Въведи имейл'}),
        'password': forms.TextInput(attrs={'placeholder': 'Въведи парола'})
    }


class CarIssueForm(forms.ModelForm):
    class Meta:
        model = CarIssue
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['problem'].required = False
        self.fields['other_issue'].required = False
        self.fields['problem'].queryset = CarProblem.objects.none()

        category_id = self.data.get(self.add_prefix('category')) or \
                      (self.instance.category_id if self.instance.pk else None)
        if category_id:
            self.fields['problem'].queryset = CarProblem.objects.filter(category_id=category_id)


class CustomerWidget(ModelSelect2Widget):
    model = Customer
    search_fields = ['first_name__icontains', 'last_name__icontains', 'phone_number__icontains']


class CarWidget(ModelSelect2Widget):
    model = Car
    search_fields = ['registration_number__icontains', 'brand__icontains', 'model__icontains']
    dependent_fields = {'customer': 'customer'}


class AcceptedCarForm(forms.ModelForm):
    class Meta:
        model = AcceptedCar
        exclude = ('date',)

        widgets = {
            'car': CarWidget(attrs={'class': 'form-control', 'data-placeholder': 'Потърси кола...'}),
            'customer': CustomerWidget(attrs={'class': 'form-control', 'data-placeholder': 'Потърси клиент...'}),
            'accepting_employee': Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'car': 'Кола',
            'customer': 'Клиент',
            'accepting_employee': 'Приемащ служител'
        }


class AcceptedCarWidget(ModelSelect2Widget):
    model = AcceptedCar
    search_fields = ['car__registration_number__icontains', 'customer__first_name__icontains']
    queryset = AcceptedCar.objects.filter(issue__isnull=True)



class IssuedCarForm(forms.ModelForm):
    class Meta:
        model = IssuedCar
        exclude = ('date',)

        widgets = {
            'accepted_car': AcceptedCarWidget(attrs={'class': 'form-control', 'data-placeholder': 'Потърси приета кола...'}),
            'mechanic': Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'accepted_car': 'Приета кола',
            'mechanic': 'Автомонтьор'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['accepted_car'].queryset = AcceptedCar.objects.filter(
                Q(issue__isnull=True) | Q(pk=self.instance.accepted_car_id)
            )


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

        widgets = {
            'registration_number': forms.TextInput(attrs={'placeholder': 'Въведи регистрационен номер'}),
            'brand': forms.TextInput(attrs={'placeholder': 'Въведи марка'}),
            'model': forms.TextInput(attrs={'placeholder': 'Въведи модел'}),
            'vin_number': forms.TextInput(attrs={'placeholder': 'Въведи ВИН номер'})
        }

        labels = {
            'registration_number': 'Регистрационен номер',
            'brand': 'Марка',
            'model': 'Модел',
            'vin_number': 'ВИН номер'
        }


class EditCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

        labels = {
            'registration_number': 'Регистрационен номер',
            'brand': 'Марка',
            'model': 'Модел',
            'vin_number': 'ВИН номер'
        }


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Въведи име'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Въведи фамилия'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Въведи телефонен номер'}),
        }

        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'phone_number': 'Телефонен номер'
        }


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        labels = {
            'first_name': 'Име',
            'last_name': 'Фамилия',
            'phone_number': 'Телефонен номер'
        }

