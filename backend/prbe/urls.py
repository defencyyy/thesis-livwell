from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('broker/login/', views.login_view_broker, name='broker_login'),
    path('broker/reset-password/', views.send_password_reset_email, name='broker_reset_password'),
    path('broker/reset-pass/<int:uid>/<str:token>/', views.BrkResetPass, name='BrkResetPass'),
    path('broker/manage-account/<int:broker_id>/', views.update_broker_view, name='update_broker'),
    path('customers/', views.add_customer, name='add_customer'),
    path('sales/total/', views.total_sales_view, name='total_sales'),
    path('sales/commissions/', views.total_commissions_view, name='total_commissions'),


    

    
    path('developer/login/', views.login_view_developer, name='developer_login'), 
    path('developer/reset-password/', views.send_dev_password_reset_email, name='developer_reset_password'),  
    path('developer/reset-pass/<int:uid>/<str:token>/', views.DevResetPass, name='DevResetPass'),

    # APIs
    path('api/companies/', include('companies.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)