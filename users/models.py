from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import os

# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    def image_upload_to(self, instance):
        if instance:
            return os.path.join("Profile_pick", self.email, instance)
        return None
    username = models.CharField(
        max_length=200, default="", blank=True, unique=False)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=150, default="", blank=False)
    last_name = models.CharField(max_length=150, default="", blank=False)
    description = models.CharField(max_length=500, default="", blank=True)
    image = models.ImageField(
        default="./default/noimage_user.jpg", upload_to=image_upload_to)
    # PONERLO EN TRUE EL IS_ACTIVE SI NO TIENE EL AUTENTICADOR DE CORREO NO ESTA CREADO AUN. CUANDO YA ESTE ,PONERLO EN FALSE COMO AHORITA ESTA
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"
        db_table = "Users"
        ordering = ("-id", )
