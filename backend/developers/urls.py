from django.urls import path
from .views import DeveloperAccountView, VerifyPasswordAPIView

urlpatterns = [
    path('', DeveloperAccountView.as_view(), name='developer_account_detail'), 
    path('verify-password/', VerifyPasswordAPIView.as_view(), name='developer_password_verify'),
]