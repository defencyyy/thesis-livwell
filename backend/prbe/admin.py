from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        if not request.user.is_authenticated:
            print(f"User is not authenticated.")
        else:
            print(f"User is authenticated.")
        
        return request.user.is_active and (request.user.is_superuser or request.user.is_staff)

custom_admin_site = CustomAdminSite(name='custom_admin')
