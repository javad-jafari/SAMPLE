from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
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