from django.db import models
from .choices import property_choices
from datetime import datetime
# from Accounts.models import User

class Property(models.Model):

  # user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=100)
  address = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  price = models.IntegerField()
  post_date = models.DateTimeField(default=datetime.now, blank=True)
  property_type = models.CharField(max_length=20, choices=property_choices, default=('house', 'House'))

  # Amenities
  # Location

  # Management
  is_active = models.BooleanField(default=True)

  # Listing
  is_listed = models.BooleanField(default=True)
  city = models.CharField(max_length=100)
  sqm = models.IntegerField()
  bedroom = models.IntegerField(default=1)
  bathroom = models.IntegerField(default=1)
  garage = models.IntegerField(default=0)
  photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
  photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  count_report = models.IntegerField(default=0, blank=True)
  
  def __str__(self):
    return self.title
  
  class Meta:
    verbose_name = "Property"         
    verbose_name_plural = "Properties"