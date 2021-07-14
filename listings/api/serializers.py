from rest_framework import serializers
from .models import Home, ZillowInfo, Address


class GetAddressSerializer(serializers.ModelSerializer):

	class Meta:
		model = Address
		exclude = []


class GetZillowIndoSerializer(serializers.ModelSerializer):

	class Meta:
		model = ZillowInfo
		exclude = []


class GetHomeSerializer(serializers.ModelSerializer):
	zillow_info = GetZillowIndoSerializer()
	address = GetAddressSerializer()

	class Meta:
		model = Home
		exclude = []