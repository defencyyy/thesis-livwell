from django.urls import path
from .views import SiteListView, SiteDetailView, StatusOptionsView, ArchivedSiteView, SiteWithFloorCountsView, SitePictureUpdateView
from .location import get_location_data

urlpatterns = [
    path('', SiteListView.as_view(), name='site-main'),
    path('<int:pk>/', SiteDetailView.as_view(), name='site-detail'),
    path('locations/', get_location_data, name='get_location_data'),
    path('status-options/', StatusOptionsView.as_view(), name='status-options'),
    path('archived/', ArchivedSiteView.as_view(), name='archived-sites-list'),
    path('archived/<int:pk>/', ArchivedSiteView.as_view(), name='archive-site'),
    path('<int:site_id>/floors/', SiteWithFloorCountsView.as_view(), name='site-floor-counts'),
    path('picture/<int:pk>/', SitePictureUpdateView.as_view(), name='site-picture-update'),
]