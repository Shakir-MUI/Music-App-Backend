# ============================================
# 2. api/models.py - Database Models
# ============================================

from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    """Store cached song information from Deezer API"""
    deezer_id = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(help_text="Duration in seconds")
    preview_url = models.URLField(max_length=500)
    cover_image = models.URLField(max_length=500)
    genre = models.CharField(max_length=100, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'songs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.artist_name}"


class Playlist(models.Model):
    """User playlists"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    songs = models.ManyToManyField(Song, related_name='playlists', blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'playlists'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} by {self.user.username}"


class Favorite(models.Model):
    """User favorite songs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'favorites'
        unique_together = ('user', 'song')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.song.title}"


class SearchHistory(models.Model):
    """Track user search history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history', null=True, blank=True)
    query = models.CharField(max_length=255)
    results_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'search_history'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.query} - {self.created_at}"