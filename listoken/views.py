from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import ListAPIView, DestroyAPIView
from knox.models import AuthToken
from listoken.serializers import ListTokenSerializer
from listoken.permissions import IsOwner
from rest_framework.permissions import IsAuthenticated



class ListTokenAPI(ListAPIView):

    queryset = AuthToken.objects.all()
    serializer_class = ListTokenSerializer 
    permission_classes = [IsAuthenticated]

    def get_object(self):
        
        return self.queryset.filter(
            user=self.request.user,
            expiry__lte=timezone.now)



class DeleteTokenAPI(DestroyAPIView):

    queryset = AuthToken.objects.all()
    permission_classes = [IsOwner]
    lookup_url_kwarg = "digest"

    def get_object(self):
        obj= get_object_or_404(
            self.get_queryset(), 
            user=self.request.user ,
            digest=self.kwargs.get("digest")
            )
        self.check_object_permissions(self.request, obj)
        return obj