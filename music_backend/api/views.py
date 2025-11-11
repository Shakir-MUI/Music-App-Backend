# ============================================
# 5. api/views.py - API Views
# ============================================

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Song, Playlist, Favorite, SearchHistory
from .serializers import (
    SongSerializer, PlaylistSerializer, 
    FavoriteSerializer, SearchHistorySerializer
)
from .services import DeezerAPIService, LRCLIBService


@api_view(['GET'])
def search_songs(request):
    """Search songs using Deezer API"""
    query = request.GET.get('q', '')
    limit = request.GET.get('limit', 20)
    
    if not query:
        return Response(
            {'error': 'Search query is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Search using Deezer API
    results = DeezerAPIService.search_tracks(query, limit)
    
    if 'error' in results:
        return Response(
            {'error': results['error']}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Save search history
    if request.user.is_authenticated:
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            results_count=len(results.get('data', []))
        )
    
    # Cache songs in database
    for track in results.get('data', []):
        Song.objects.update_or_create(
            deezer_id=track['id'],
            defaults={
                'title': track['title'],
                'artist_name': track['artist']['name'],
                'album_name': track.get('album', {}).get('title', ''),
                'duration': track['duration'],
                'preview_url': track['preview'],
                'cover_image': track.get('album', {}).get('cover_medium', ''),
            }
        )
    
    return Response(results)


@api_view(['GET'])
def get_track_details(request, track_id):
    """Get detailed track information"""
    track_data = DeezerAPIService.get_track_details(track_id)
    
    if 'error' in track_data:
        return Response(
            {'error': track_data['error']}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response(track_data)


@api_view(['GET'])
def get_lyrics(request):
    """Fetch lyrics for a song"""
    track_name = request.GET.get('track')
    artist_name = request.GET.get('artist')
    album_name = request.GET.get('album', None)
    duration = request.GET.get('duration', None)
    
    if not track_name or not artist_name:
        return Response(
            {'error': 'Track name and artist name are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Try to get lyrics from LRCLIB
    lyrics_data = LRCLIBService.get_lyrics(
        track_name, artist_name, album_name, duration
    )
    
    if 'error' in lyrics_data:
        # Fallback to search
        lyrics_data = LRCLIBService.search_lyrics(
            track_name, artist_name, album_name
        )
    
    if not lyrics_data or 'error' in lyrics_data:
        return Response(
            {'message': 'Lyrics not found for this song'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response(lyrics_data)


class PlaylistViewSet(viewsets.ModelViewSet):
    """ViewSet for Playlist CRUD operations"""
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_song(self, request, pk=None):
        """Add a song to playlist"""
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        
        try:
            song = Song.objects.get(id=song_id)
            playlist.songs.add(song)
            return Response({'message': 'Song added to playlist'})
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def remove_song(self, request, pk=None):
        """Remove a song from playlist"""
        playlist = self.get_object()
        song_id = request.data.get('song_id')
        
        try:
            song = Song.objects.get(id=song_id)
            playlist.songs.remove(song)
            return Response({'message': 'Song removed from playlist'})
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class FavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet for managing favorite songs"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def create(self, request):
        """Add a song to favorites"""
        song_id = request.data.get('song_id')
        
        try:
            song = Song.objects.get(id=song_id)
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                song=song
            )
            
            if created:
                return Response(
                    {'message': 'Song added to favorites'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'Song already in favorites'},
                    status=status.HTTP_200_OK
                )
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['delete'])
    def remove(self, request):
        """Remove a song from favorites"""
        song_id = request.data.get('song_id')
        
        try:
            favorite = Favorite.objects.get(
                user=request.user, 
                song_id=song_id
            )
            favorite.delete()
            return Response({'message': 'Song removed from favorites'})
        except Favorite.DoesNotExist:
            return Response(
                {'error': 'Favorite not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
def get_search_history(request):
    """Get user's search history"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Authentication required'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    history = SearchHistory.objects.filter(user=request.user)[:20]
    serializer = SearchHistorySerializer(history, many=True)
    return Response(serializer.data)