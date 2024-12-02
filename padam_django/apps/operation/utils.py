import datetime

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from padam_django.apps.fleet.models import Bus, Driver
from padam_django.apps.operation.models import BusShift


def is_overlapping(
    shifts: QuerySet["BusShift"], current_interval: tuple[datetime.time, datetime.time]
) -> bool:
    shift_ranges = [
        (shift.start_time, shift.finish_time)
        for shift in shifts
        if shift.start_time and shift.finish_time
    ]

    for shift in shift_ranges:
        if (
            shift[0] <= current_interval[0] < shift[1]
            or shift[0] < current_interval[1] <= shift[1]
        ):
            return True
    return False


def check_bus_overlapping(
    bus: Bus, bus_shift: BusShift, current_interval: tuple[datetime.time, datetime.time]
) -> None:
    shifts = bus.bus_shifts.exclude(id=bus_shift.id)
    if is_overlapping(shifts, current_interval):
        raise ValidationError("Bus times overlap")


def check_driver_overlapping(
    driver: Driver,
    bus_shift: BusShift,
    current_interval: tuple[datetime.time, datetime.time],
) -> None:
    shifts = driver.bus_shifts.exclude(id=bus_shift.id)
    if is_overlapping(shifts, current_interval):
        raise ValidationError("Driver times overlap")
