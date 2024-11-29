from django.db import models
from companies.models import Company

class Milestone(models.Model):
    STATUS_CHOICES = [
        ('sales', 'Sales'),
        ('commission', 'Commission'),
    ]

    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    reward = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sales')
    sales_threshold = models.PositiveIntegerField(null=True, blank=True)  # Number of sales required
    commission_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Commission amount required
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.name