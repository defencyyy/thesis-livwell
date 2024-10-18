from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Admin view
    path('admin/', admin.site.urls),

    # Broker 
    path('broker/login/', views.login_view, name='broker-login'),  # Login for brokers
    path('broker/reset-password/', views.send_password_reset_email, name='broker-reset-password'),  # Forgot password
    path('broker/resetpass/<int:uid>/<str:token>/', views.BrokResetPass, name='broker-reset-pass'),  # Password reset

    # Developer
    path('developer/login/', views.login_view_dev, name='developer-login'),  # Login for developers
    path('developer/reset-password/', views.send_dev_password_reset_email, name='developer-reset-password'),  # Forgot password
    path('developer/resetpass/<int:uid>/<str:token>/', views.DevResetPass, name='developer-reset-pass'),  # Password reset
]
