from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from knox.models import AuthToken
import re


def password_validator(value):
    passwd = 'Geek12@'
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
      
    # compiling regex
    pat = re.compile(reg)
      
    # searching regex                 
    mat = re.search(pat, passwd)
    if mat:
        raise ValidationError(
            _('%(value)s must include numbers, chars, signs'),
            params={'value': value},
        )        
    elif len(value) < 5 :
        raise ValidationError(
            _('%(value)s should be more than 5 digit'),
            params={'value': value},
        )

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        if not phone:
            raise ValueError('The given phone must be set')
    
        user = self.model(username=username, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username,phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username,phone, password, **extra_fields)

    def create_superuser(self,username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(_('password'), max_length=128, validators=[password_validator])
    username = models.CharField(_('username'), max_length=100,unique=True)
    phone = models.CharField(_('phone'), max_length=11,unique=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        

class LoginToken(models.Model):

    agent = models.CharField(max_length=2000)
    digest = models.ForeignKey(AuthToken, on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return self.agent




