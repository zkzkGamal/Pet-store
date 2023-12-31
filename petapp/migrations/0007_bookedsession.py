# Generated by Django 4.1.1 on 2023-06-04 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0006_doctorvent_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookedsession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessionData', models.DateTimeField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.doctorvent')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.profile')),
            ],
        ),
    ]
