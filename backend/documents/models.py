from django.db import models
from companies.models import Company
from customers.models import Customer
from sales.models import Sale
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os, re

def document_file_upload_path(instance, filename):
    company_name = instance.company.name if instance.company else 'new_company'
    customer_id = instance.customer.id if instance.customer else 'unknown_customer'
    customer_name = instance.customer.name if instance.customer else 'unknown_customer'
    
    # Replace spaces with underscores and strip special characters from the customer name
    customer_name = re.sub(r'\s+', '_', customer_name)
    customer_name = re.sub(r'[^\w\s-]', '', customer_name)
    
    # Ensure filename has a default value if None
    filename = filename or 'default.pdf'
    
    # Extract file extension from the original filename
    file_extension = os.path.splitext(filename)[1]
    
    document_type_name = instance.document_type.name if instance.document_type else 'unknown_type'
    
    filename = f"{document_type_name}{file_extension}"
    
    return os.path.join('files', str(company_name), f"{customer_id}_{customer_name}", filename)

# DocumentType model for dynamically adding document types
class DocumentType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50, unique=True)  # e.g., 'Contract', 'Deed', 'Brochure'
    description = models.TextField(blank=True, null=True)  # Optional description of the document type

    def __str__(self):
        return self.name

class Document(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    description = models.CharField(max_length=200,blank=True)
    file = models.FileField(upload_to=document_file_upload_path)  # Custom upload path
    uploaded_at = models.DateTimeField(auto_now_add=True)
    sales = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='documents')  # Adding the sales id as a FK
    # Link to DocumentType for flexible types
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.document_type}"

