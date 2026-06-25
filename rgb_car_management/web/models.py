from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from scipy._lib.cobyqa.problem import Problem

from rgb_car_management.web.managers import RgbCarManagementUserManager
from rgb_car_management.web.validators import contains_only_letters_validator


class Employee(AbstractBaseUser, PermissionsMixin):
    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 2

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            contains_only_letters_validator
        ),
    )
    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            contains_only_letters_validator
        ),
    )
    email = models.EmailField(
        unique=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_superuser = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = RgbCarManagementUserManager()

    def __str__(self):
        return self.email


class Customer(models.Model):
    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 2

    MAX_INTEGERS_PER_NUMBER = 20

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            contains_only_letters_validator
        ),
    )
    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            contains_only_letters_validator
        ),
    )
    phone_number = models.CharField(
        max_length=MAX_INTEGERS_PER_NUMBER,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Car(models.Model):
    MAX_REGISTRATION_NUMBER_LENGTH = 8
    MIN_REGISTRATION_NUMBER_LENGTH = 7

    MAX_BRAND_LENGTH = 20
    MIN_BRAND_LENGTH = 2

    MAX_MODEL_LENGTH = 20

    VIN_NUMBER_LENGTH = 17

    registration_number = models.CharField(
        max_length=MAX_REGISTRATION_NUMBER_LENGTH,
        validators=(
            MinLengthValidator(MIN_REGISTRATION_NUMBER_LENGTH),
        ),
    )
    brand = models.CharField(
        max_length=MAX_BRAND_LENGTH,
        validators=(
            MinLengthValidator(MIN_BRAND_LENGTH),
        ),
    )
    model = models.CharField(
        max_length=MAX_MODEL_LENGTH,
    )
    vin_number = models.CharField(
        max_length=VIN_NUMBER_LENGTH,
        validators=(
            MinLengthValidator(VIN_NUMBER_LENGTH),
        ),
    )

    def __str__(self):
        return f'{self.registration_number}'


class CarIssueCategory(models.Model):
    MAX_CATEGORY_CHOICES_LENGTH = 100

    category = models.CharField(
        max_length=MAX_CATEGORY_CHOICES_LENGTH,
    )
    is_other = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.category


class CarProblem(models.Model):
    MAX_NAME_LENGTH = 100

    category = models.ForeignKey(
        CarIssueCategory,
        on_delete=models.CASCADE,
        related_name='problems',
    )
    name = models.CharField(
        max_length=MAX_NAME_LENGTH
    )

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return self.name


class CarIssue(models.Model):
    MAX_OTHER_ISSUE_LENGTH = 100

    category = models.ForeignKey(
        CarIssueCategory,
        on_delete=models.CASCADE,
        related_name='issues_category',
    )
    problem = models.ForeignKey(
        CarProblem,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='issues_problems',
    )
    other_issue = models.TextField(
        max_length=MAX_OTHER_ISSUE_LENGTH,
        blank=True,
        null=True,
    )

    def clean(self):
        if not self.category_id:
            return
        if self.category.is_other:
            if not self.other_issue:
                raise ValidationError({'other_issue': 'Опиши проблема!'})
            else:
                self.problem = None
        else:
            if not self.problem:
                raise ValidationError({'problem': 'Избери проблем!'})
            if self.problem.category_id != self.category_id:
                raise ValidationError({'problem': 'Този проблем не е от тази категория!'})
            self.other_issue = None

    def __str__(self):
        return self.other_issue or (self.problem.name if self.problem else self.category.category)


class AcceptedCar(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
    )
    accepting_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='accepted_cars_ae',
    )
    date = models.DateTimeField(
        auto_now_add=True,
    )
    car = models.OneToOneField(
        Car,
        on_delete=models.CASCADE,
    )
    issues = models.ManyToManyField(
        CarIssue,
        related_name='accepted_cars_i',
    )

    def __str__(self):
        return f'{str(self.customer)} - {str(self.car)}'



class IssuedCar(models.Model):
    accepted_car = models.OneToOneField(
        AcceptedCar,
        on_delete=models.CASCADE,
    )
    mechanic = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='accepted_cars_m',
    )
    repairs = models.ManyToManyField(
        CarIssue,
        related_name='issued_cars',
    )
    date = models.DateTimeField(
        auto_now_add=True,
    )


