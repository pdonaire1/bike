# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-16 04:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bikes', '0001_initial'),
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_rental_from', models.IntegerField()),
                ('count_rental_to', models.IntegerField()),
                ('percentaje_discount', models.IntegerField()),
                ('name', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bikes.Bike')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Client')),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.Promotion')),
            ],
        ),
        migrations.CreateModel(
            name='RentalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('length', models.CharField(max_length=80)),
            ],
        ),
        migrations.AddField(
            model_name='rental',
            name='rental_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentals.RentalType'),
        ),
    ]