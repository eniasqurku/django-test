import factory
from faker import Faker

from . import models

fake = Faker()


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory("padam_django.apps.fleet.factories.BusFactory")
    driver = factory.SubFactory("padam_django.apps.fleet.factories.DriverFactory")

    class Meta:
        model = models.BusShift


class BusStopFactory(factory.django.DjangoModelFactory):
    place = factory.SubFactory("padam_django.apps.geography.factories.PlaceFactory")
    bus_shift = factory.SubFactory(
        "padam_django.apps.operation.factories.BusShiftFactory"
    )
    schedule_time = factory.Faker("time")

    class Meta:
        model = models.BusStop
