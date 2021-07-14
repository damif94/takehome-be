from rest_framework import generics

from .models import Home
from .serializers import GetHomeSerializer


class HomeList(generics.ListAPIView):
	queryset = Home.objects.all()
	serializer_class = GetHomeSerializer
