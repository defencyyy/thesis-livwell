from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    def has_permission(self, request):
        if not request.user.is_authenticated:
            print(f"User is not authenticated: {request.user.username}")
        else:
            print(f"Authenticated user: {request.user.username}")
            print(f"is_active: {request.user.is_active}")
            print(f"is_superuser: {request.user.is_superuser}")
            print(f"is_staff: {request.user.is_staff}")
        return request.user.is_active and (request.user.is_superuser or request.user.is_staff)

        

custom_admin_site = CustomAdminSite(name='custom_admin')