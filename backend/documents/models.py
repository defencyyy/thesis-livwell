from django.db import models
from companies.models import Company
from customers.models import Customer
from sales.models import Sale
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os, re

def document_file_upload_path(instance, filename):
    company_name = instance.company.name if instance.company else 'new_company'
    customer_code = instance.customer.customer_code if instance.customer else 'unknown_customer'
    customer_name = instance.customer.name if instance.customer else 'unknown_customer'
    
    company_name = re.sub(r'\s+', '', company_name) 
    company_name = re.sub(r'[^\w\s-]', '', company_name) 
    customer_name = re.sub(r'\s+', '', customer_name)
    customer_name = re.sub(r'[^\w\s-]', '', customer_name)
    document_type_name = instance.document_type.name if instance.document_type else 'unknown_type'
    document_type_name = re.sub(r'\s+', '', document_type_name)
    document_type_name = re.sub(r'[^\w\s-]', '', document_type_name)
    
    # Ensure filename has a default value if None
    filename = filename or 'default.pdf'
    
    # Extract file extension from the original filename
    file_extension = os.path.splitext(filename)[1]
    
    # Add Sale ID, Document Type, and file extension to the filename
    sale_id = instance.sales.id if instance.sales else 'unknown_sale'
    
    # Create the new filename format: sale_id_document_type_name_file_extension
    filename = f"{sale_id}_{document_type_name}{file_extension}"
    
    return os.path.join('files', str(company_name), f"{customer_code}_{customer_name}", filename)

# DocumentType model for dynamically adding document types
class DocumentType(models.Model):
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)  # Removed 'unique=True' here
    description = models.TextField(blank=True, null=True)  # Optional description of the document type

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'name'], name='unique_document_type_per_company')
        ]

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

