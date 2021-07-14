from rest_framework import generics

from .models import Home
from .serializers import GetHomeSerializer
from django_filters import rest_framework as filters


class HomeFilter(filters.FilterSet):
	home_size__lt = filters.NumberFilter(field_name="home_size", lookup_expr="lt")
	home_size__gt = filters.NumberFilter(field_name="home_size", lookup_expr="gt")

	state = filters.CharFilter(field_name="address__state", lookup_expr="iexact")

	zillow_price__lt = filters.NumberFilter(field_name="zillow_info__price", lookup_expr="lt")
	zillow_price__gt = filters.NumberFilter(field_name="zillow_info__price", lookup_expr="gt")

	class Meta:
		model = Home
		fields = '__all__'


class HomeList(generics.ListAPIView):
	queryset = Home.objects.all()
	serializer_class = GetHomeSerializer
	filter_backends = [filters.DjangoFilterBackend]
	filterset_class = HomeFilter
