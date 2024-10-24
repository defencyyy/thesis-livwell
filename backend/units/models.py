from django.db import models
from companies.models import Company
from affiliations.models import Affiliation
from sites.models import Site

class Unit(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
    ]
    VIEW_CHOICES = [
        ('south', 'South'),
        ('north', 'North'),
        ('east', 'East'),
        ('west', 'West'),
    ]
    BALCONY_CHOICES = [
        ('has_balcony', 'Has Balcony'),
        ('no_balcony', 'No Balcony'),
    ]

    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    site = models.ForeignKey(Site, on_delete=models.DO_NOTHING)
    affiliations = models.ManyToManyField(Affiliation, related_name='units')
    title = models.CharField(max_length=100)
    floor_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    lot_area = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    floor = models.PositiveIntegerField(default=1, help_text="Floor number")
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    view = models.CharField(max_length=10, choices=VIEW_CHOICES, blank=True)
    balcony = models.CharField(max_length=20, choices=BALCONY_CHOICES, blank=True)
    commission = models.DecimalField(
      max_digits=10, decimal_places=2, null=True, 
      help_text="Commission earned when the unit is sold"
    )

    def __str__(self):
        return f"{self.site.name} - {self.title}"
