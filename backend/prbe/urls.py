from django.contrib import admin
from django.urls import path
from . import view




urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', view.login_view, name='login'),
    path('reset-password/', view.send_password_reset_email, name='reset-password'),
    path('reset-password-confirm/<int:uid>/<str:token>/', view.reset_password_confirm, name='password_reset_confirm'),

]
