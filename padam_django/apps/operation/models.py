import datetime

from dateutil.relativedelta import relativedelta
from django.db import models

from padam_django.apps.fleet.models import Bus


# Create your models here.
class BusStop(models.Model):
    place = models.ForeignKey(
        "geography.Place", on_delete=models.CASCADE, related_name="bus_stops"
    )
    bus_shift = models.ForeignKey(
        "BusShift", on_delete=models.CASCADE, related_name="bus_stops"
    )
    schedule_time = models.TimeField("time of arrival/departure")

    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Bus stop"
        verbose_name_plural = "Bus stops"
        ordering = ["order", "schedule_time"]
        unique_together = ["place", "bus_shift", "schedule_time"]

    def __str__(self):
        """We should be careful here because there will be multiple
        calls to the db for joining place and bus shift for every busStop
        It only affects django admin list view. For the purpose of this assignment we
        can leave it like this."""
        return f"BusStop: {self.place.name} - {self.bus_shift}"


class BusShift(models.Model):
    bus = models.ForeignKey(
        "fleet.Bus", on_delete=models.CASCADE, related_name="bus_shifts"
    )
    driver = models.ForeignKey(
        "fleet.Driver", on_delete=models.CASCADE, related_name="bus_shifts"
    )

    class Meta:
        verbose_name = "Bus shift"
        verbose_name_plural = "Bus shifts"

    def __str__(self):
        return f"BusShift {self.id}: {self.bus} - {self.driver} / {self.start_time}-{self.finish_time}"

    @property
    def start_time(self) -> datetime.time | None:
        first_stop = self.bus_stops.first()
        return first_stop.schedule_time if first_stop else None

    @property
    def finish_time(self) -> datetime.time | None:
        last_stop = self.bus_stops.last()
        return last_stop.schedule_time if last_stop else None

    @property
    def travel_time(self) -> relativedelta:
        start_time = self.start_time
        finish_time = self.finish_time
        if not (start_time and finish_time):
            return relativedelta(minutes=0)

        # convert to datetime momentarily in order to get the timedelta
        d1, d2 = datetime.datetime.now(), datetime.datetime.now()
        d1 = d1.replace(hour=start_time.hour, minute=start_time.minute)
        d2 = d2.replace(hour=finish_time.hour, minute=finish_time.minute)

        # in case the finish time is earlier than start time then
        # it means that the schedule spans across 2 days hence why
        # we add 1 day to the finish datetime
        if d2 < d1:
            d2 = d2 + relativedelta(days=1)

        return relativedelta(d2, d1)
