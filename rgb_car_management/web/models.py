from django.core.validators import MinLengthValidator
from django.db import models

from rgb_car_management.web.validators import contains_only_letters_validator


class Customer(models.Model):
    MAX_FIRST_NAME_LENGTH = 20
    MIN_FIRST_NAME_LENGTH = 2

    MAX_LAST_NAME_LENGTH = 20
    MIN_LAST_NAME_LENGTH = 2

    MAX_INTEGERS_PER_NUMBER = 10
    MIN_INTEGERS_PER_NUMBER = 10

    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_FIRST_NAME_LENGTH),
            contains_only_letters_validator
        ),
    )
    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_LAST_NAME_LENGTH),
            contains_only_letters_validator
        ),
    )
    phone_number = models.IntegerField(
        max_length=MAX_INTEGERS_PER_NUMBER,
        validators=(
            MinLengthValidator(MIN_INTEGERS_PER_NUMBER),
        ),
    )


class Car(models.Model):
    MAX_REGISTRATION_NUMBER_LENGTH = 10
    MIN_REGISTRATION_NUMBER_LENGTH = 8

    MAX_BRAND_LENGTH = 20
    MIN_BRAND_LENGTH = 2

    MAX_MODEL_LENGTH = 20

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


class CarExamination(models.Model):
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
    examinations = models.CharField()
    is_ready = models.BooleanField(
        default=False,
    )


class CarReady(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField(
        auto_now_add=True,
    )
    fixes = models.CharField()
    price = models.PositiveIntegerField()
    with_invoice = models.BooleanField(
        default=False,
    )

