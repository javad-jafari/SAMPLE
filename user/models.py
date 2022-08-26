from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from user.validators import password_validator, phone_validator
from user.managers import UserManager
from knox.models import AuthToken




class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(_('password'), max_length=128, validators=[password_validator])
    username = models.CharField(_('username'), max_length=100,unique=True)
    phone = models.CharField(_('phone'), max_length=11,unique=True, validators=[phone_validator])

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

    agent = models.CharField(max_length=128)
    digest = models.ForeignKey(AuthToken, on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return self.agent




