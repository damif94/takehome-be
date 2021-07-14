from typing import Optional

from django.core.management.base import BaseCommand
import csv
from api.models import Address, Home, ZillowInfo
from datetime import datetime
import pytz


def unit_multiplier(n, unit) -> int:
    if unit == "M":
        return n*1000000
    elif unit == "K":
        return n*1000
    raise NotImplementedError


def date_parser(date: str) -> Optional[datetime]:
    date = date.split("/")
    if len(date) == 1:
        return None
    return datetime(year=int(date[2]),month=int(date[0]),day=int(date[1]),tzinfo=pytz.UTC)


class Command(BaseCommand):
    help = 'Imports data about houses'

    def add_arguments(self, parser):
        parser.add_argument("-s", "--strict", action="store_true", help="Gets the homes with all fields not null")

    def handle(self, *args, **options):
        with open("../sample-data/data.csv", mode="r") as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:

                if options["strict"] and any([v == '' for v in row.values()]):
                    continue

                address = Address.objects.create(
                    street=" ".join(row["address"].split(" ")[1:]),
                    number=row["address"].split(" ")[0],
                    zipcode=row["zipcode"],
                    state=row["state"],
                )

                zillow_info = ZillowInfo.objects.create(
                    zillow_id=row["zillow_id"],
                    last_sold_date=date_parser(row["last_sold_date"]),
                    last_sold_price=row["last_sold_price"] or None,
                    _link=row["link"][len(ZillowInfo.zillow_base_link):],
                    rent_price=row["rent_price"] or None, #vacio
                    rent_estimate_price=row["rentzestimate_amount"] or None,
                    rent_estimate_price_last_updated=date_parser(row["rentzestimate_last_updated"]),
                    price=unit_multiplier(float(row["price"][1:-1]), row["price"][-1]),
                    price_estimate=row["zestimate_amount"] or None,
                    price_estimate_last_updated=date_parser(row["zestimate_last_updated"]),
                    tax_value=int(float(row["tax_value"])) if row["tax_value"] else None,
                    tax_year=row["tax_year"],
                )

                Home.objects.create(
                    n_bathrooms=row["bathrooms"] or None,
                    n_bedrooms=row["bedrooms"],
                    home_size=row["home_size"] or None,
                    property_size=row["property_size"] or None,
                    home_type=row["home_type"],
                    year_built=row["year_built"] or None,
                    zillow_info=zillow_info,
                    address=address
                )

        self.stdout.write("Import finished")
