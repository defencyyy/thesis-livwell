from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', view.login_view, name='login'),
    path('reset-password/', view.send_password_reset_email, name='reset-password'),
    path('brokpass/<int:uid>/<str:token>/', view.BrokResetPass, name='BrokResetPass'),
]
