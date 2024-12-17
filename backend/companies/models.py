from django.db import models
import os, re

def logo_upload_path(instance, filename):
    company_name = instance.name if instance.name else 'new_company'  
    company_name = re.sub(r'\s+', '', company_name) 
    company_name = re.sub(r'[^\w\s-]', '', company_name) 

    filename = 'company_logo.jpg' 

    return os.path.join('photos', str(company_name), 'logo', filename)


class Company(models.Model):
  name = models.CharField(max_length=100, unique=True, editable=True)
  description = models.TextField(blank=True)
  is_active = models.BooleanField(default=True)
  logo = models.ImageField(upload_to=logo_upload_path, blank=True) 
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
  
  def delete_old_logo(self):
      if self.pk:  # Ensure the object already exists (has been saved before)
          try:
              old_logo = Company.objects.get(pk=self.pk).logo
              if old_logo and old_logo != self.logo:
                  if os.path.isfile(old_logo.path):
                      os.remove(old_logo.path)  # Remove old file
          except Company.DoesNotExist:
              pass

  def save(self, *args, **kwargs):
      self.delete_old_logo()  # Call to delete the old logo before saving the new one
      super().save(*args, **kwargs)

  def delete(self, *args, **kwargs):
    # Delete the logo when the company instance is deleted
    if self.logo and os.path.isfile(self.logo.path):
      os.remove(self.logo.path)
      super().delete(*args, **kwargs)

  class Meta:
    verbose_name = "Company"
    verbose_name_plural = "Companies"

