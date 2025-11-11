from django.contrib import admin
from .models import Song, Playlist, Favorite, SearchHistory


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    """Admin interface for Song model"""
    list_display = ['title', 'artist_name', 'album_name', 'duration', 'genre', 'created_at']
    list_filter = ['genre', 'created_at']
    search_fields = ['title', 'artist_name', 'album_name']
    readonly_fields = ['deezer_id', 'created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Song Information', {
            'fields': ('deezer_id', 'title', 'artist_name', 'album_name')
        }),
        ('Media', {
            'fields': ('preview_url', 'cover_image')
        }),
        ('Details', {
            'fields': ('duration', 'genre', 'release_date')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition of songs (they come from API)"""
        return False


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    """Admin interface for Playlist model"""
    list_display = ['name', 'user', 'song_count', 'is_public', 'created_at', 'updated_at']
    list_filter = ['is_public', 'created_at', 'user']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['songs']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Playlist Information', {
            'fields': ('user', 'name', 'description', 'is_public')
        }),
        ('Songs', {
            'fields': ('songs',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def song_count(self, obj):
        """Display number of songs in playlist"""
        return obj.songs.count()
    song_count.short_description = 'Number of Songs'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Admin interface for Favorite model"""
    list_display = ['user', 'get_song_title', 'get_artist_name', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'song__title', 'song__artist_name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_song_title(self, obj):
        """Display song title"""
        return obj.song.title
    get_song_title.short_description = 'Song Title'
    
    def get_artist_name(self, obj):
        """Display artist name"""
        return obj.song.artist_name
    get_artist_name.short_description = 'Artist'


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    """Admin interface for SearchHistory model"""
    list_display = ['query', 'user', 'results_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['query', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        """Prevent manual addition (auto-generated)"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent editing"""
        return False


# Customize admin site header and title
admin.site.site_header = "Music App Administration"
admin.site.site_title = "Music App Admin"
admin.site.index_title = "Welcome to Music App Admin Panel"