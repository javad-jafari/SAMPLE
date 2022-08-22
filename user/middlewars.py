from django.utils.deprecation import MiddlewareMixin
from rest_framework import exceptions


class FilterAgentMiddleware(MiddlewareMixin):
    # Check if client IP is allowed
    def process_request(self, request):
       
        if  request.META['HTTP_USER_AGENT']:
            # If user agent was in header we don't do anything
            return None
        raise exceptions.PermissionDenied() # If user is not allowed raise Error
 
