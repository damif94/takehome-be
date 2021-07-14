from django.db import models
from .enums import HouseType


class ZillowInfo(models.Model):
	"""model for persisting house data related to zillow provider"""
	zillow_id = models.IntegerField()
	last_sold_date = models.DateTimeField(null=True)
	last_sold_price = models.IntegerField(null=True)
	_link = models.SlugField()
	rent_price = models.IntegerField(null=True)
	rent_estimate_price = models.IntegerField(null=True, help_text="zillow own estimation for the monthly rent price")
	rent_estimate_price_last_updated = models.DateTimeField(null=True)
	price = models.IntegerField()
	price_estimate = models.IntegerField(null=True, help_text="zillow own estimation for the price")
	price_estimate_last_updated = models.DateTimeField(null=True)
	tax_value = models.IntegerField()  # not inherent to the house because update may depend on provider
	tax_year = models.IntegerField()

	zillow_base_link = "https://www.zillow.com/homedetails/"

	@property
	def link(self) -> str:
		return self.zillow_base_link + str(self._link)


class Address(models.Model):  # if new models like buildings were added; it could be convenient to let this independent
	street = models.CharField(max_length=50)
	number = models.IntegerField()
	zipcode = models.IntegerField()
	state = models.CharField(max_length=2)

	class Meta:
		indexes = [
			models.Index(fields=["state", "zipcode"]),
		]
		# this index allows (state) or (state,zip_address) filter, as stated
		# https://stackoverflow.com/questions/45328826/django-model-fields-indexing


class Home(models.Model):
	"""model for persisting home inherent data"""
	n_bathrooms = models.FloatField(null=True)
	n_bedrooms = models.IntegerField()
	home_size = models.IntegerField(null=True, help_text="the home size measures in square feet")
	property_size = models.IntegerField(null=True, help_text="the whole property size measures in square feet")
	home_type = models.CharField(max_length=30, choices=[(type,type) for type in list(HouseType)])
	year_built = models.IntegerField(null=True)
	zillow_info = models.ForeignKey(null=True, on_delete=models.SET_NULL, to=ZillowInfo)
	address = models.ForeignKey(null=False, on_delete=models.RESTRICT, to=Address)

	class Meta:
		indexes = [
			models.Index(fields=["year_built"]),
			models.Index(fields=["home_size"]),
			models.Index(fields=["property_size"]),
		]
