from django.contrib import admin
from .models import Developer
from prbe.admin import custom_admin_site  # Use custom admin site
from django.utils.translation import gettext_lazy as _


class DeveloperTypeFilter(admin.SimpleListFilter):
    """
    Filter to separate Superusers and Regular Developers.
    """
    title = _('Developer Type')
    parameter_name = 'developer_type'

    def lookups(self, request, model_admin):
        return (
            ('regular', _('Developers')),
            ('superuser', _('Admins')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'regular':
            return queryset.filter(is_superuser=False)
        if self.value() == 'superuser':
            return queryset.filter(is_superuser=True)
        return queryset


@admin.register(Developer, site=custom_admin_site)
class DeveloperAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Developer model.
    """
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'company', 'contact_number', 'is_superuser')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company__name')
    list_per_page = 25
    list_filter = (DeveloperTypeFilter, 'company')

    fieldsets = (
        (None, {
            'fields': ('company', 'username', 'email', 'password'),
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'contact_number'),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {
            'fields': ('last_login',),
        }),
    )

    def get_queryset(self, request):
        """
        Restrict regular developers to see only non-superusers.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all developers
        return qs.filter(is_superuser=False)

    def has_module_permission(self, request):
        """
        Restrict access to this admin module based on user type.
        """
        if request.user.is_superuser:
            return True  # Superusers have full module access
        return False  # Regular developers cannot access modules directly

    def has_change_permission(self, request, obj=None):
        """
        Allow change permission for own data or by superusers.
        """
        if obj is None:
            return True  # Allows access to the change list view
        if request.user.is_superuser:
            return True  # Superusers can change any record
        return obj == request.user  # Regular developers can only change their own record

    def has_delete_permission(self, request, obj=None):
        """
        Allow deletion permission only for superusers.
        """
        if request.user.is_superuser:
            return True
        return False  # Regular developers cannot delete

    def save_model(self, request, obj, form, change):
        """
        Automatically associate a new developer with default permissions or groups.
        """
        super().save_model(request, obj, form, change)
        if not change and not obj.is_superuser:
            # Assign default group for regular developers (if such a group exists)
            from django.contrib.auth.models import Group
            group = Group.objects.filter(name='Developers').first()
            if group:
                obj.groups.add(group)
