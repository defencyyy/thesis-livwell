from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .admin import custom_admin_site
from . import views

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    # Route for reset password (this is where users will be redirected with the reset token)
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),

    # Brokers
    path('broker/login/', views.login_view_broker, name='broker_login'),
    path('broker/manage-accounts/<int:broker_id>/', views.get_broker_data, name='get_broker_data'),
    path('broker/manage-account/<int:broker_id>/', views.update_broker_view, name='update_broker'),
    path('customers/', views.add_customer, name='add_customer'),
    path('sales/total/', views.total_sales_view, name='total_sales'),
    path('sales/commissions/', views.total_commissions_view, name='total_commissions'),
    path('sales/sites/', views.site_sales_view, name='site_sales'),  
    path('sales/details/', views.sales_details_view, name='sales-details'),
    path('brokers/<int:broker_id>/', views.get_broker, name='get_broker'),
    path('sites/available/', views.get_available_sites, name='get_available_sites'),
    path('units/available/', views.get_available_units, name='get_available_units'),  
    path('sites/<int:site_id>/', views.get_site_name, name='get_site_name'),  
    path('customers/broker/<int:broker_id>/', views.get_customers_for_broker, name='get_customers_for_broker'),
    path('sites/', views.fetch_sites, name='fetch_sites'),
    path('units/site/<int:site_id>/', views.fetch_units, name='fetch_units'),
    path('sales/', views.fetch_sales, name='fetch_sales'),
    path('reserve-unit/', views.reserve_unit, name='reserve-unit'),
    path('submit-sales/', views.submit_sales, name='submit_sales'),
    path('sales-detail/<uuid:sales_detail_id>/', views.get_sales_detail, name='view_sales_detail'),
    path('download_reservation_agreement/<int:sales_detail_id>/', views.download_reservation_agreement, name='download_reservation_agreement'),
    path('salesdetails/check/<int:customer_id>/<int:site_id>/<int:unit_id>/', views.check_sales_details, name='check_sales_details'),
    path('document-types/', views.fetch_document_types, name='fetch_document_types'),
    path('upload-document/', views.upload_document, name='upload_document'),
    path('documents/customer/<int:customer_id>/<int:sales_id>/', views.fetch_customer_documents, name='fetch_customer_documents'),
    path('customers/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('mark/<int:customer_id>/<int:sales_id>/', views.mark_unit_as_sold, name='mark_unit_as_sold'),
    path('milestones/', views.get_milestones, name='get_milestones'),
    path('delete_sale/<int:sale_id>/', views.delete_sale, name='delete_sale'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('sales/by-month/', views.sales_by_month, name='sales_by_month'),
    path('units/<int:unit_id>/details', views.get_unit_details, name='get_unit_details'),

    # PRBE

    # Developers
    # API Endpoints
    path('api/token/developer/', views.login_view_developer, name='login_developer'),
    path('api/token/devlogout/', views.dev_logout_view, name='developer_logout'),
    path('api/token/brklogout/', views.brk_logout_view, name='broker_logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('developer/company/', include('companies.urls')),  
    path('developer/brokers/', include('brokers.urls')), 
    path('developer/sites/', include('sites.urls')),
    path('developer/account/', include('developers.urls')), 
    path('developer/customers/', include('customers.urls')), 
    path('developer/documents/', include('documents.urls')), 
    path('developer/milestones/', include('milestones.urls')), 
    path('developer/sales/', include('sales.urls')), 
    path('developer/units/', include('units.urls')), 
    path('developer/dashboard/', include('dashboard.urls')), 
    # # path('api/token/broker/', views.login_view_broker, name='login_broker'), 
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
