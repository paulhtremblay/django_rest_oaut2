from django.db import models

class DOB(models.Model):
    name = models.CharField(max_length=100, blank=False)
    dob = models.DateField(blank = False)
    class Meta:
        managed = True
        db_table = 'henry_dob'

class NotManaged(models.Model):
    name = models.CharField(max_length=100, blank=False, primary_key = True)
    dob = models.DateField(blank = False)
    class Meta:
        managed = False
        db_table = 'old_dob'

