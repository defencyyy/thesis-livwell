from django.contrib import admin
from .models import Developer
from prbe.admin import custom_admin_site  # Use custom admin site
from django.utils.translation import gettext_lazy as _

# Custom filter to separate Superusers and Regular Developers
class DeveloperTypeFilter(admin.SimpleListFilter):
    title = _('Developer Type')
    parameter_name = 'developer_type'

    def lookups(self, request, model_admin):
        return (
            ('regular', _('Developers')),
            ('superuser', _('Admin')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'regular':
            return queryset.filter(is_superuser=False)
        if self.value() == 'superuser':
            return queryset.filter(is_superuser=True)
        return queryset

class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'first_name', 'last_name', 'email', 'contact_number')
    list_display_links = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'company__name', 'email', 'username')
    list_per_page = 25

    # Add filter for Superusers vs Regular Developers
    list_filter = (DeveloperTypeFilter,)

    def get_queryset(self, request):
        """Return queryset based on user type."""
        if request.user.is_superuser:
            return Developer.objects.all()  # Superuser can see all developers
        else:
            return Developer.objects.filter(is_superuser=False)  # Regular developers only see non-superusers

    def has_module_permission(self, request):
        """Restrict access to Django admin modules."""
        if request.user.is_superuser:
            return True  # Superusers can access all modules
        return False  # Regular developers cannot access other modules like auth, sessions, etc.

    def has_change_permission(self, request, obj=None):
        """Allow change permission only for developers to their own data."""
        if obj is None:
            return False  # No change permission for all developers to others' data
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Allow delete permission only for developers to their own data."""
        if obj is None:
            return False  # No delete permission for all developers
        return super().has_delete_permission(request, obj)

# Register the Developer model with the custom admin site
custom_admin_site.register(Developer, DeveloperAdmin)
