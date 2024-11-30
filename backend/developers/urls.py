from django.urls import path
from .views import DeveloperAccountView

urlpatterns = [
    path('', DeveloperAccountView.as_view(), name='developer_account_detail'), 
]