from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator
from django.db import models

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


class CarIssue(models.Model):
    ISSUE_CHOICES = (
        ('broken engine', 'broken engine'),
        ('other', 'other'),
    )

    MAX_ISSUE_CHOICES_LENGTH = max([len(i) for i, _ in ISSUE_CHOICES])

    MAX_OTHER_ISSUE_LENGTH = 100

    issue = models.CharField(
        max_length=MAX_ISSUE_CHOICES_LENGTH,
        choices=ISSUE_CHOICES,
    )
    other_issue = models.TextField(
        max_length=MAX_OTHER_ISSUE_LENGTH,
        blank=True,
        null=True,
    )
    is_ready = models.BooleanField(
        default=False,
    )

    def __str__(self):
        if self.other_issue:
            return self.other_issue
        else:
            return self.issue


class AcceptedCar(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
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
        related_name='accepted_cars',
    )
    is_ready = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f'{str(self.customer)} - {str(self.car)}'




class IssuedCar(models.Model):
    accepted_car = models.OneToOneField(
        AcceptedCar,
        on_delete=models.CASCADE,
    )
    fixes = models.CharField()
    date = models.DateTimeField(
        auto_now_add=True,
    )


