from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    alterado = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True

class UsuarioManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        user=self._create_user(email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


class Usuario(Base):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=255)
    is_anonymous = models.BooleanField()
    is_authenticated = models.BooleanField()


    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['senha']

    objects = UsuarioManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"