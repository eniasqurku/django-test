# Generated by Django 3.2.5 on 2021-07-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Place",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=50, verbose_name="Name of the place"),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        decimal_places=6, max_digits=9, verbose_name="Longitude"
                    ),
                ),
                (
                    "latitude",
                    models.DecimalField(
                        decimal_places=6, max_digits=9, verbose_name="Latitude"
                    ),
                ),
            ],
            options={
                "unique_together": {("longitude", "latitude")},
            },
        ),
    ]
