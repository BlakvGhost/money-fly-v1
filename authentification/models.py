from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email doit être spécifié.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    account_num = models.CharField(max_length=255, unique=True)
    balance = models.FloatField(max_length=255, default=0, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token_expiration = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def can_send(self, balance):
        return self.is_superuser or (self.balance >= balance)
    
    def is_reset_token_valid(self, token):
        return self.reset_token == token

    def is_reset_token_expired(self):
        return self.reset_token_expiration is not None and self.reset_token_expiration < timezone.now()
    
    def serialise(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_login,
            'account_num': self.account_num,
            'balance': self.balance,
        }