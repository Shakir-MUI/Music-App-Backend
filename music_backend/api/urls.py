# ============================================
# 6. api/urls.py - URL Configuration
# ============================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'playlists', views.PlaylistViewSet, basename='playlist')
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', views.search_songs, name='search-songs'),
    path('track/<int:track_id>/', views.get_track_details, name='track-details'),
    path('lyrics/', views.get_lyrics, name='get-lyrics'),
    path('search-history/', views.get_search_history, name='search-history'),
]