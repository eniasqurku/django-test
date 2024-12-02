import datetime

from adminsortable2.admin import (
    SortableTabularInline,
    SortableAdminBase,
)
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import (
    inlineformset_factory,
    ModelForm,
)

from padam_django.apps.operation.models import BusStop, BusShift
from padam_django.apps.operation.utils import (
    check_bus_overlapping,
    check_driver_overlapping,
)


class BusStopsInLineAdmin(SortableTabularInline):
    model = BusStop
    extra = 1


class BusShiftForm(ModelForm):
    class Meta:
        model = BusShift
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        BusStopFormSet = inlineformset_factory(
            BusShift,
            BusStop,
            fields=("place", "schedule_time", "order"),
            extra=0,
        )

        # Instantiate the formset with the saved bus shift
        formset = BusStopFormSet(self.data, instance=self.instance)

        if formset.is_valid():
            # check if bus and/or driver overlap with another shift
            bus_stop_schedules: list[datetime.time] = [
                bus_stop["schedule_time"]
                for bus_stop in sorted(
                    formset.cleaned_data, key=lambda x: x.get("order", 0)
                )
                if bus_stop and not bus_stop["DELETE"]
            ]
            if bus_stop_schedules:
                interval = bus_stop_schedules[0], bus_stop_schedules[-1]
                check_bus_overlapping(cleaned_data["bus"], self.instance, interval)
                check_driver_overlapping(
                    cleaned_data["driver"], self.instance, interval
                )
        else:
            # If formset is not valid, raise validation error
            raise ValidationError(formset.errors)

        return cleaned_data


class BusShiftAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [BusStopsInLineAdmin]
    form = BusShiftForm
    list_select_related = ["bus", "driver"]
    list_display = ["id", "bus", "driver", "travel_time"]

    def travel_time(self, obj: BusShift):
        travel_time = obj.travel_time
        return f"{travel_time.days} days - {travel_time.hours} hours - {travel_time.minutes} mins"


# Register your models here.
admin.site.register(BusShift, BusShiftAdmin)
