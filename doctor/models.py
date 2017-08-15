# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Doctor(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    npi = models.CharField(max_length=20)


class Practice(models.Model):
    doctor = models.ForeignKey(Doctor)
    street = models.CharField(max_length=64)
    street_2 = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)