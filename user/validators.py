from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from config.settings import PHONE_PATTERN
import re


def password_validator(value):

    # compiling regex
    pat = re.compile(PHONE_PATTERN)
      
    # searching regex                 
    mat = re.search(pat, value)
    if not mat:
        raise ValidationError(
            _('%(value)s must include numbers, chars, signs'),
            params={'value': value},
        )        
    elif len(value) < 5 :
        raise ValidationError(
            _('%(value)s should be more than 5 '),
            params={'value': value},
        )