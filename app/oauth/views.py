from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import parsers
from .serializers import ProfileSerializer
from .models import CustomUser


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,]
    parser_classes = (parsers.MultiPartParser,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return CustomUser.objects.filter(user=self.request.user)