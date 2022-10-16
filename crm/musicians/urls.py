from django.urls import path
from .views import (musician_list, musician_detail, musician_create, musician_update, musician_delete, MusicianListView, MusicianDetailView, MusicianCreateView,MusicianUpdateView, MusicianDeleteView, AssignBandView, CategoryListView
)

app_name = "musicians"

urlpatterns = [
path('', MusicianListView.as_view(), name='musician-list'),
path('<int:pk>/', MusicianDetailView.as_view(), name='musician-detail'),
path('<int:pk>/update/', MusicianUpdateView.as_view(), name='musician-update'),
path('<int:pk>/delete/', MusicianDeleteView.as_view(), name='musician-delete'),
path('create/', MusicianCreateView.as_view(), name='musician-create'),
path('create/', MusicianCreateView.as_view(), name='musician-create'),
path('<int:pk>/assign-band/', AssignBandView.as_view(), name='assign-band'),
path('categories/', CategoryListView.as_view(), name='category-list'),
path('categories/<int:pk>/', CategoryListView.as_view(), name='category-detail'),
]
