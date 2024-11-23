from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group, Permission
from django.contrib.admin import site as default_admin_site

class CustomAdminSite(AdminSite):
    def has_permission(self, request):        
        return request.user.is_active and (request.user.is_superuser or request.user.is_staff)

custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(Group)
custom_admin_site.register(Permission)
