from django.db import models
from companies.models import Company
from affiliations.models import Affiliation
from sites.models import Site
from decimal import Decimal

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

    @classmethod
    def create_dummy_data(cls):
        # Create dummy data
        units_data = [
            {
                "title": "1-Bedroom Unit",
                "floor_area": Decimal("35.00"),
                "lot_area": Decimal("45.00"),
                "floor": 2,
                "quantity": 5,
                "status": "available",
                "price": Decimal("2500000.00"),
                "view": "south",
                "balcony": "has_balcony",
                "commission": Decimal("250000.00"),
                "company_id": 1,  # Replace with actual Company ID
                "site_id": 1,     # Replace with actual Site ID
            },
            {
                "title": "2-Bedroom Unit",
                "floor_area": Decimal("55.00"),
                "lot_area": Decimal("60.00"),
                "floor": 3,
                "quantity": 8,
                "status": "sold",
                "price": Decimal("3800000.00"),
                "view": "east",
                "balcony": "no_balcony",
                "commission": Decimal("300000.00"),
                "company_id": 1,  # Replace with actual Company ID
                "site_id": 1,     # Replace with actual Site ID
            },
            {
                "title": "Studio Unit",
                "floor_area": Decimal("25.00"),
                "lot_area": Decimal("30.00"),
                "floor": 5,
                "quantity": 5,
                "status": "available",
                "price": Decimal("1800000.00"),
                "view": "west",
                "balcony": "no_balcony",
                "commission": Decimal("180000.00"),
                "company_id": 1,  # Replace with actual Company ID
                "site_id": 1,     # Replace with actual Site ID
            },
        ]

        # Insert the data into the database
        for unit in units_data:
            cls.objects.create(**unit)
