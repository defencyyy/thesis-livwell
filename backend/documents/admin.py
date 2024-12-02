from django.contrib import admin
from .models import Document, DocumentType
from sales.models import Sale
from customers.models import Customer
from companies.models import Company
from django.contrib.contenttypes.models import ContentType
from prbe.admin import custom_admin_site  # Use custom admin site
from django.utils.translation import gettext_lazy as _

class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('company', 'customer', 'document_type', 'uploaded_at', 'get_related_sales')
    list_display_links = ('company', 'customer')
    search_fields = ('customer__name', 'company__name', 'document_type__name')
    list_per_page = 25
    list_filter = ('company', 'customer', 'document_type')

    # Remove filter_horizontal since 'sales' is not a ManyToManyField
    # Add related Sales in the list display using a custom method
    def get_related_sales(self, obj):
        # Check if the document has an associated sale
        if obj.sales:
            return str(obj.sales.id)  # Or you can return other properties of Sale like `obj.sales.name`
        return "No sale linked"
    get_related_sales.short_description = 'Related Sales'

    # Add content_type and object_id for Generic Foreign Key in the form
    fieldsets = (
        (None, {
            'fields': ('company', 'customer', 'description', 'document_type', 'file', 'sales')
        }),
      
    )
    # Remove filter_horizontal for 'sales' as it's a ForeignKey, not ManyToMany
    # This will use the default form widget for ForeignKey (dropdown selection)
    # filter_horizontal = ('sales',)  # REMOVE THIS LINE

    def save_model(self, request, obj, form, change):
        """
        Automatically associate a document with related sales or set content_type and object_id.
        """
        super().save_model(request, obj, form, change)
        
        # If no content_type or object_id set, set them based on the sales relationship
        if not obj.content_type and not obj.object_id and obj.sales:
            obj.content_type = ContentType.objects.get_for_model(Sale)
            obj.object_id = obj.sales.id  # Set content_type and object_id based on the sales field
            
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """
        Restrict access to documents based on user type and permissions.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all documents
        return qs.filter(customer__user=request.user)  # Regular users can only see their own documents

    def has_module_permission(self, request):
        """
        Restrict access to this admin module based on user type.
        """
        if request.user.is_superuser:
            return True  # Superusers have full module access
        return False  # Regular users cannot access the module directly

    def has_change_permission(self, request, obj=None):
        """
        Allow change permission for own data or by superusers.
        """
        if obj is None:
            return True  # Allows access to the change list view
        if request.user.is_superuser:
            return True  # Superusers can change any record
        return obj.customer.user == request.user  # Users can only edit their own documents

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion permission only for superusers.
        """
        if request.user.is_superuser:
            return True
        return False  # Regular developers cannot delete

# Register the models with the custom admin site
custom_admin_site.register(DocumentType, DocumentTypeAdmin)
custom_admin_site.register(Document, DocumentAdmin)
