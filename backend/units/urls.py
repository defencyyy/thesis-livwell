from django.urls import path
from .views import UnitListView, UnitDetailView, UnitTemplateListView, UnitTemplateDetailView, UnitTypeListView, UnitTypeDetailView, BulkAddUnitsView

urlpatterns = [
    # Unit URLs
    path('', UnitListView.as_view(), name='unit-list'),
    path('<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('bulk-add/', BulkAddUnitsView.as_view(), name='unit-bulk-add'),
    path('templates/', UnitTemplateListView.as_view(), name='unit-template-list'),
    path('templates/<int:pk>/', UnitTemplateDetailView.as_view(), name='unit-template-detail'),
    path('types/', UnitTypeListView.as_view(), name='unit-type-list'), 
    path('types/<int:pk>/', UnitTypeDetailView.as_view(), name='unit-type-detail'),  
    
]
