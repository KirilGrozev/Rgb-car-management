from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from rgb_car_management.web.models import Car, Customer, AcceptedCar, IssuedCar, Employee


class RegisterUserForm(UserCreationForm):
    user = None

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields = ('first_name', 'last_name', 'email')

        label = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

    widgets = {
        'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
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
            'username': 'Email',
            'password': 'Password'
        }

    widgets = {
        'username': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        'password': forms.TextInput(attrs={'placeholder': 'Enter Password'})
    }


class CreateAcceptedCarForm(forms.ModelForm):
    class Meta:
        model = AcceptedCar
        exclude = ('date',)


class EditAcceptedCarForm(forms.ModelForm):
    class Meta:
        model = AcceptedCar
        fields = '__all__'


class CreateIssuedCarForm(forms.ModelForm):
    class Meta:
        model = IssuedCar
        exclude = ('date',)


class EditIssuedCarForm(forms.ModelForm):
    class Meta:
        model = IssuedCar
        fields = '__all__'


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class EditCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

