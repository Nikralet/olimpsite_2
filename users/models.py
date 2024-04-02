from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(blank=True, unique=True, verbose_name="Номер телефона")

    #  БАЛЛЫ буду делать здесь
    loyalty_program = models.PositiveIntegerField(verbose_name="Баллы программы лояльности", default=0)

