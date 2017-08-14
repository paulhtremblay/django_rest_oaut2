from django.db import models

class DOB(models.Model):
    name = models.CharField(max_length=100, blank=False)
    dob = models.DateField(blank = False)

# Create your models here.
