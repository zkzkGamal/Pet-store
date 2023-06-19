# Generated by Django 4.1.7 on 2023-04-03 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "petapp",
            "0002_order_alter_product_product_catecory_shippingaddress_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="DoctorVent",
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
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.TextField(blank=True, max_length=11, null=True)),
                ("vent_phone", models.TextField(blank=True, max_length=11, null=True)),
                ("address", models.TextField(blank=True, null=True)),
                ("profile_pic", models.ImageField(upload_to="")),
                ("about", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="petapp.profile",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="petapp.order",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="petapp.product",
            ),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="customer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="petapp.profile",
            ),
        ),
        migrations.AlterField(
            model_name="shippingaddress",
            name="order",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="petapp.order",
            ),
        ),
        migrations.CreateModel(
            name="Vent_Photo",
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
                ("vent_img", models.FileField(upload_to="")),
                (
                    "DoctorVent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="petapp.doctorvent",
                    ),
                ),
            ],
            options={
                "verbose_name": "Vent_Photo",
                "verbose_name_plural": "Vent_Photos",
            },
        ),
    ]
