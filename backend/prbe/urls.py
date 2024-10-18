from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', view.login_view, name='login'),
    path('reset-password/', view.send_password_reset_email, name='reset-password'),#for brokers
    path('brokpass/<int:uid>/<str:token>/', view.BrokResetPass, name='BrokResetPass'),#for brokers
    path('devlogin/', view.login_view_dev, name='devlogin'),  # for developers
    path('reset-dev-password/', view.send_dev_password_reset_email, name='reset-dev-password'),  # for developers
    path('devpass/<int:uid>/<str:token>/', view.DevResetPass, name='DevResetPass'),  # for developers
]
