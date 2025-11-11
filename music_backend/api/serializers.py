
# ============================================
# 3. api/serializers.py - Data Serialization
# ============================================

from rest_framework import serializers
from .models import Song, Playlist, Favorite, SearchHistory
from django.contrib.auth.models import User


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, read_only=True)
    song_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 'songs', 'song_count', 'is_public', 'created_at', 'updated_at']
    
    def get_song_count(self, obj):
        return obj.songs.count()


class FavoriteSerializer(serializers.ModelSerializer):
    song = SongSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'song', 'created_at']


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = '__all__'