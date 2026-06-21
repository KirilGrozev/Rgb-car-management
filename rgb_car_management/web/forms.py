from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_select2 import forms as select2_forms

from rgb_car_management.web.models import Car, Customer, AcceptedCar, IssuedCar, Employee, CarIssue


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


class AcceptedCarForm(forms.ModelForm):
    selected_issues = forms.MultipleChoiceField(
        choices=CarIssue.ISSUE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'issue-checkbox',
            'onchange': 'toggleOtherFields()'
        }),
        required=True,
        label='Избери проблемите по колата'
    )

    other_issue_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'other-description',
            'rows': 3,
            'placeholder': 'Въведи друг проблем по колата',
            'style': 'display:none;'
        }),
        required=False,
        label='Друг проблем по колата'
    )

    class Meta:
        model = AcceptedCar
        exclude = ('date',)

        widgets = {
            'car': select2_forms.Select2Widget(attrs={'class': 'form-control', 'data-placeholder': 'Потърси кола...'}),
            'customer': select2_forms.Select2Widget(attrs={'class': 'form-control', 'data-placeholder': 'Потърси клиент...'}),
        }

        labels = {
            'car': 'Кола',
            'customer': 'Клиент',
        }

    def clean(self):
        cleaned_data = super().clean()
        selected_issues = cleaned_data.get('selected_issues')
        other_issue_description = cleaned_data.get('other_issue_description')

        if selected_issues and 'other' in selected_issues:
            if not other_issue_description or not other_issue_description.strip():
                raise forms.ValidationError(
                    'Моля поясни проблема след като си избрал "Друго"! '
                )

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        instance.issues.clear()

        selected_issues = self.cleaned_data.get('selected_issues', [])
        other_issue = self.cleaned_data.get('other_issue_description', '')

        for issue_type in selected_issues:
            if issue_type == 'other':
                car_issue = CarIssue.objects.create(
                    issue='other',
                    other_issue=other_issue
                )
            else:
                car_issue = CarIssue.objects.create(
                    issue=issue_type
                )

            instance.issues.add(car_issue)

        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            existing_issues = self.instance.issues.all()

            selected_issue_types = list(existing_issues.values_list('problem_type', flat=True))

            self.fields['selected_issues'].initial = selected_issue_types

            other_issue = existing_issues.filter(problem_type='other').first()

            if other_issue and other_issue.other_description:
                self.fields['other_issue_description'].initial = other_issue.other_description


class CreateIssuedCarForm(forms.ModelForm):
    class Meta:
        model = IssuedCar
        exclude = ('date',)

        widgets = {
            'accepted_car': select2_forms.Select2Widget(attrs={'class': 'form-control', 'data-placeholder': 'Потърси приета кола...'}),
        }

        labels = {
            'accepted_car': 'Приета кола',
        }


class EditIssuedCarForm(forms.ModelForm):
    class Meta:
        model = IssuedCar
        fields = '__all__'

        labels = {
            'accepted_car': 'Приета кола'
        }


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

