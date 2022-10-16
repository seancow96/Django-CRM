from django.urls import path
from .views import BandsListView, BandCreateView, BandUpdateView, BandDeleteView, BandDetailView
app_name = 'bands'

urlpatterns = [
    path('', BandsListView.as_view(), name="band-list"),
    path('<int:pk>/', BandDetailView.as_view(), name='band-detail'),
    path('create/', BandCreateView.as_view(), name='band-create'),
    path('<int:pk>/update/', BandUpdateView.as_view(), name='band-update'),
    path('<int:pk>/delete/', BandDeleteView.as_view(), name='band-delete'),

]