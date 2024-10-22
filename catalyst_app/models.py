from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    year_founded = models.IntegerField()
    industry = models.CharField(max_length=255)
    size_range = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    linkedin_url = models.CharField(max_length=255)
    current_employee_estimate = models.IntegerField()
    total_employee_estimate = models.IntegerField()


    # Add fields matching your CSV data
