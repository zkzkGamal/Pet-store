# Generated by Django 4.1.1 on 2023-05-28 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0003_doctorvent_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startsession', models.DateTimeField()),
                ('endsession', models.DateTimeField()),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='petapp.doctorvent')),
            ],
        ),
    ]