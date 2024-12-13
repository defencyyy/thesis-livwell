from django.urls import path
from .views import UnitListView, UnitDetailView, UnitTemplateListView, UnitTemplateDetailView, UnitTypeListView, UnitTypeDetailView, BulkAddUnitsView, UnitsBySectionView, ImageManagementView, ImageUploadView

urlpatterns = [
    # Unit URLs
    path('', UnitListView.as_view(), name='unit-list'),
    path('<int:pk>/', UnitDetailView.as_view(), name='unit-detail'),
    path('bulk-add/', BulkAddUnitsView.as_view(), name='unit-bulk-add'),
    path('templates/', UnitTemplateListView.as_view(), name='unit-template-list'),
    path('templates/<int:pk>/', UnitTemplateDetailView.as_view(), name='unit-template-detail'),
    path('types/', UnitTypeListView.as_view(), name='unit-type-list'), 
    path('types/<int:pk>/', UnitTypeDetailView.as_view(), name='unit-type-detail'),  
    path('<int:site_id>/sections/<int:section_id>/', UnitsBySectionView.as_view(), name='units-by-sections'),
    path('<int:unit_id>/images/', ImageUploadView.as_view(), name='upload_image'),
    path('<int:unit_id>/images/<int:image_id>/', ImageManagementView.as_view(), name='manage_image'),
]
