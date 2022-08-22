import site
from django.contrib import admin
from user.models import User,LoginToken



admin.site.register(User)
admin.site.register(LoginToken)
