from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("e-mail", unique=True)
    name = models.CharField("nome", max_length=150)
    phone = models.CharField("telefone", max_length=20, blank=True)

    is_active = models.BooleanField("ativo", default=True)
    is_staff = models.BooleanField("acesso ao admin do Django", default=False)
    date_joined = models.DateTimeField("cadastrado em", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]  # pedidos no createsuperuser (além de e-mail e senha)

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
