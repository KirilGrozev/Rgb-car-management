from django import forms

from rgb_car_management.web.models import CarExamination, CarReady, Car, Customer


class CreateCarExaminationForm(forms.ModelForm):
    class Meta:
        model = CarExamination
        exclude = ('date',)


class EditCarExaminationForm(forms.ModelForm):
    class Meta:
        model = CarExamination
        fields = '__all__'


class CreateReadyCarForm(forms.ModelForm):
    class Meta:
        model = CarReady
        exclude = ('date',)


class EditReadyCarForm(forms.ModelForm):
    class Meta:
        model = CarExamination
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

