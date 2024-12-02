from django.urls import path
from .views import UnitListView, UnitDetailView, UnitTemplateListView, UnitTemplateDetailView

urlpatterns = [
    # Unit URLs
    path('', UnitListView.as_view(), name='unit-list'),
    path('<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('templates/', UnitTemplateListView.as_view(), name='unit-template-list'),
    path('templates/<int:pk>/', UnitTemplateDetailView.as_view(), name='unit-template-detail'),
]
