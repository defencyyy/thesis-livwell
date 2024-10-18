from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('broker/login/', views.login_view, name='broker_login'),
    path('broker/reset-password/', views.send_password_reset_email, name='broker_reset_password'),
    path('broker/reset-pass/<int:uid>/<str:token>/', views.BrkResetPass, name='BrkResetPass'),
    
    path('developer/login/', views.login_view_dev, name='developer_login'), 
    path('developer/reset-password/', views.send_dev_password_reset_email, name='developer_reset_password'),  
    path('developer/reset-pass/<int:uid>/<str:token>/', views.DevResetPass, name='DevResetPass'),
]
