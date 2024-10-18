from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('reset-password/', views.send_password_reset_email, name='reset-password'),#for brokers
    path('brokpass/<int:uid>/<str:token>/', views.BrokResetPass, name='BrokResetPass'),#for brokers
    path('devlogin/', views.login_view_dev, name='devlogin'),  # for developers
    path('reset-dev-password/', views.send_dev_password_reset_email, name='reset-dev-password'),  # for developers
    path('devpass/<int:uid>/<str:token>/', views.DevResetPass, name='DevResetPass'),  # for developers
]
