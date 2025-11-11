# ============================================
# 4. api/services.py - External API Services
# ============================================

import requests
from django.conf import settings


class DeezerAPIService:
    """Service to interact with Deezer API"""
    BASE_URL = "https://api.deezer.com"
    
    @staticmethod
    def search_tracks(query, limit=20):
        """Search for tracks on Deezer"""
        try:
            url = f"{DeezerAPIService.BASE_URL}/search"
            params = {
                'q': query,
                'limit': limit
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'data': []}
    
    @staticmethod
    def get_track_details(track_id):
        """Get detailed information about a specific track"""
        try:
            url = f"{DeezerAPIService.BASE_URL}/track/{track_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_artist_info(artist_id):
        """Get artist information"""
        try:
            url = f"{DeezerAPIService.BASE_URL}/artist/{artist_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_album_info(album_id):
        """Get album information"""
        try:
            url = f"{DeezerAPIService.BASE_URL}/album/{album_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}


class LRCLIBService:
    """Service to fetch lyrics from LRCLIB (free and open)"""
    BASE_URL = "https://lrclib.net/api"
    
    @staticmethod
    def search_lyrics(track_name, artist_name, album_name=None):
        """Search for lyrics by track and artist name"""
        try:
            url = f"{LRCLIBService.BASE_URL}/search"
            params = {
                'track_name': track_name,
                'artist_name': artist_name,
            }
            if album_name:
                params['album_name'] = album_name
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json()
            
            # Return the first result if available
            if results and len(results) > 0:
                return results[0]
            return None
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_lyrics(track_name, artist_name, album_name=None, duration=None):
        """Get lyrics with more specific matching"""
        try:
            url = f"{LRCLIBService.BASE_URL}/get"
            params = {
                'track_name': track_name,
                'artist_name': artist_name,
            }
            if album_name:
                params['album_name'] = album_name
            if duration:
                params['duration'] = duration
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}