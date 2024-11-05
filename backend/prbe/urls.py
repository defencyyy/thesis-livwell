from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Brokers
    path('broker/login/', views.login_view_broker, name='broker_login'),
    path('broker/reset-password/', views.send_password_reset_email, name='broker_reset_password'),
    path('broker/reset-pass/<int:uid>/<str:token>/', views.BrkResetPass, name='BrkResetPass'),
    # path('broker/logout/', views.brk_logout_view, name='broker_logout'),
    path('broker/manage-account/<int:broker_id>/', views.update_broker_view, name='update_broker'),
    path('customers/', views.add_customer, name='add_customer'),
    path('sales/total/', views.total_sales_view, name='total_sales'),
    path('sales/commissions/', views.total_commissions_view, name='total_commissions'),
    path('sales/sites/', views.site_sales_view, name='site_sales'),  
    path('sales/details/', views.sales_details_view, name='sales-details'),
    path('brokers/<int:broker_id>/', views.get_broker, name='get_broker'),
    path('sites/available/', views.get_available_sites, name='get_available_sites'),
    path('units/available/', views.get_available_units, name='get_available_units'),  # Add the new URL pattern
    path('sites/<int:site_id>/', views.get_site_name, name='get_site_name'),  # URL pattern for fetching site name



    

    # Developers
    path('developer/login/', views.login_view_developer, name='developer_login'), 
    path('developer/reset-password/', views.send_dev_password_reset_email, name='developer_reset_password'),  
    path('developer/reset-pass/<int:uid>/<str:token>/', views.DevResetPass, name='DevResetPass'),
    path('developer/logout/', views.dev_logout_view, name='developer_logout'),
    path('developer/company/', include('companies.urls')),


]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)