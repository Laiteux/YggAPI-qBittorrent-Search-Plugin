# VERSION: 2.0
# AUTHORS: Laiteux (matt@laiteux.dev)
# CONTRIBUTORS: Sterbweise (contact@sterbweise.dev)

"""
YggAPI qBittorrent Search Plugin
Modern Python implementation with automatic YggTorrent URL discovery

Features:
- Automatic YggTorrent URL fetching from https://yeeti.io/@ygg
- Smart URL caching (24 hours)
- 60+ YggTorrent categories supported
- Robust error handling with retry logic
- Modern Python code with type hints

Category Support:
- Standard qBittorrent categories (all, movies, tv, music, games, anime, software, pictures, books)
- Extended YggTorrent categories (animation, documentary, manga, emulation, etc.)
- Direct category ID support (e.g., "2183" for films)

Configuration:
- Set your PASSKEY in the YggAPIConfig class
- Customize search parameters (per_page, order_by, max_retries, etc.)
- Adjust URL cache duration if needed
"""

import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlencode, quote_plus
from helpers import retrieve_url
from novaprinter import prettyPrinter


class YggAPIConfig:
    """
    Configuration manager for YggAPI plugin
    
    This class contains all configuration settings for the YggAPI search plugin,
    including category mappings for 60+ YggTorrent categories organized by content type.
    
    To configure your passkey:
    1. Set YGG_PASSKEY environment variable, OR
    2. Edit PASSKEY below, OR
    3. Create a file named 'yggapi_passkey.txt' in the same directory
    """
    
    # API Configuration
    API_BASE_URL: str = "https://yggapi.eu"
    
    # Passkey configuration (multiple methods supported)
    # Priority: 1. Environment variable, 2. Config file, 3. Hardcoded value
    @staticmethod
    def _get_passkey() -> str:
        """Get passkey from multiple sources (env var > file > hardcoded)"""
        # Try environment variable first
        env_passkey = os.environ.get('YGG_PASSKEY', '').strip()
        if env_passkey:
            return env_passkey
        
        # Try config file
        try:
            passkey_file = Path(__file__).parent / 'yggapi_passkey.txt'
            if passkey_file.exists():
                with open(passkey_file, 'r', encoding='utf-8') as f:
                    file_passkey = f.read().strip()
                    if file_passkey:
                        return file_passkey
        except (OSError, IOError):
            pass
        
        # Fallback to hardcoded value
        return "YOUR_PASSKEY_HERE"  # Change this or use env var/file method
    
    PASSKEY: str = _get_passkey.__func__()
    
    # Yeeti.io configuration for automatic URL discovery
    YEETI_PROFILE_URL: str = "https://yeeti.io/@ygg"
    URL_CACHE_FILE: str = ".ygg_url_cache.json"
    URL_CACHE_DURATION_HOURS: int = 24
    
    # Search Configuration
    DEFAULT_PER_PAGE: int = 100
    DEFAULT_ORDER_BY: str = "seeders"
    MAX_RETRIES: int = 3
    RETRY_DELAY_SECONDS: int = 2
    REQUEST_TIMEOUT: int = 30
    
    # Category Mappings (qBittorrent -> YggTorrent)
    CATEGORY_MAPPING: Dict[str, str] = {
        "all": "",
        "movies": "2183",
        "tv": "2184",
        "music": "2148",
        "games": "2142",
        "anime": "2179",
        "software": "2144",
        "pictures": "2191",
        "books": "2140"
    }
    
    # Complete YggTorrent Category Mappings
    # Format: category_id -> category_name
    YGG_CATEGORY_NAMES: Dict[str, str] = {
        # Films & Vidéos (2145)
        "2145": "films-videos",
        "2178": "animation",
        "2179": "animation-série",
        "2180": "concert",
        "2181": "documentaire",
        "2182": "emission-tv",
        "2183": "film",
        "2184": "série-tv",
        "2185": "spectacle",
        "2186": "sport",
        "2187": "video-clip",
        
        # Ebook (2140)
        "2140": "ebook",
        "2151": "ebook-audio",
        "2152": "bds",
        "2153": "comics",
        "2154": "livres",
        "2155": "manga",
        "2156": "presse",
        
        # Audio (2139)
        "2139": "audio",
        "2147": "karaoke",
        "2148": "musique",
        "2149": "samples",
        "2150": "podcast-radio",
        
        # XXX (2188)
        "2188": "xxx",
        "2401": "xxx-ebooks",
        "2189": "xxx-films",
        "2190": "hentai",
        "2191": "xxx-images",
        "2402": "xxx-jeux",
        
        # Jeux vidéo (2142)
        "2142": "jeu-video",
        "2167": "jeu-autre",
        "2159": "jeu-linux",
        "2160": "jeu-macos",
        "2162": "jeu-microsoft",
        "2163": "jeu-nintendo",
        "2165": "jeu-smartphone",
        "2164": "jeu-sony",
        "2166": "jeu-tablette",
        "2161": "jeu-windows",
        
        # Applications (2144)
        "2144": "application",
        "2177": "app-autre",
        "2176": "formation",
        "2171": "app-linux",
        "2172": "app-macos",
        "2174": "app-smartphone",
        "2175": "app-tablette",
        "2173": "app-windows",
        
        # Nulled (2300)
        "2300": "nulled",
        "2304": "nulled-divers",
        "2303": "nulled-mobile",
        "2302": "scripts-php-cms",
        "2301": "wordpress",
        
        # Imprimante 3D (2200)
        "2200": "imprimante-3d",
        "2201": "3d-objets",
        "2202": "3d-personnages",
        
        # GPS (2143)
        "2143": "gps",
        "2168": "gps-applications",
        "2169": "gps-cartes",
        "2170": "gps-divers",
        
        # Émulation (2141)
        "2141": "emulation",
        "2157": "emulateur",
        "2158": "rom-iso"
    }
    
    # Extended Category Mappings for direct ID access
    # Allows searching by specific subcategories
    EXTENDED_CATEGORY_MAPPING: Dict[str, str] = {
        # Films & Vidéos
        "animation": "2178",
        "animation_series": "2179",
        "concert": "2180",
        "documentary": "2181",
        "tv_show": "2182",
        "movie": "2183",
        "series": "2184",
        "show": "2185",
        "sport": "2186",
        "videoclip": "2187",
        
        # Ebook categories
        "audiobook": "2151",
        "comics": "2153",
        "books": "2154",
        "manga": "2155",
        "press": "2156",
        
        # Audio categories
        "karaoke": "2147",
        "samples": "2149",
        "podcast": "2150",
        
        # Gaming platforms
        "games_linux": "2159",
        "games_mac": "2160",
        "games_microsoft": "2162",
        "games_nintendo": "2163",
        "games_sony": "2164",
        "games_windows": "2161",
        
        # Applications
        "training": "2176",
        "software_linux": "2171",
        "software_mac": "2172",
        "software_windows": "2173",
        
        # Nulled/Development
        "nulled": "2300",
        "wordpress": "2301",
        "php_scripts": "2302",
        
        # 3D Printing
        "3d_printing": "2200",
        "3d_objects": "2201",
        "3d_characters": "2202",
        
        # GPS & Navigation
        "gps": "2143",
        "gps_apps": "2168",
        "gps_maps": "2169",
        
        # Emulation
        "emulation": "2141",
        "emulator": "2157",
        "roms": "2158"
    }


class URLCache:
    """Manages caching of the YggTorrent URL"""
    
    def __init__(self, cache_file: str, cache_duration_hours: int):
        self._cache_file = Path(cache_file)
        self._cache_duration = timedelta(hours=cache_duration_hours)
    
    def get_cached_url(self) -> Optional[str]:
        """Retrieve cached URL if still valid"""
        if not self._cache_file.exists():
            return None
        
        try:
            with open(self._cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            cached_time = datetime.fromisoformat(cache_data.get('timestamp', ''))
            cached_url = cache_data.get('url', '')
            
            if datetime.now() - cached_time < self._cache_duration and cached_url:
                return cached_url
        except (json.JSONDecodeError, ValueError, OSError):
            pass
        
        return None
    
    def save_url(self, url: str) -> None:
        """Save URL to cache with timestamp"""
        cache_data = {
            'url': url,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            with open(self._cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f)
        except OSError:
            pass  # Silently fail if cache cannot be written


class YggURLFetcher:
    """Fetches the current YggTorrent URL from yeeti.io"""
    
    def __init__(self, profile_url: str, cache: URLCache):
        self._profile_url = profile_url
        self._cache = cache
    
    def get_ygg_url(self, fallback_url: str = "https://www.yggtorrent.org") -> str:
        """
        Get the current YggTorrent URL from yeeti.io/@ygg bio
        Falls back to cached URL or default URL if fetch fails
        """
        # Try cache first
        cached_url = self._cache.get_cached_url()
        if cached_url:
            return cached_url
        
        # Try to fetch from yeeti.io
        try:
            response = retrieve_url(self._profile_url)
            
            # Parse the bio/website field from the yeeti.io profile
            # Look for patterns like https://www.yggtorrent.*/
            url_patterns = [
                r'https?://(?:www\.)?yggtorrent\.[a-z]{2,}/?',
                r'<meta\s+property=["\']og:url["\']\s+content=["\'](https?://[^"\']*yggtorrent[^"\']*)["\']',
                r'href=["\'](https?://[^"\']*yggtorrent[^"\']*)["\']',
                r'"website"\s*:\s*"(https?://[^"]*yggtorrent[^"]*)"'
            ]
            
            for pattern in url_patterns:
                matches = re.findall(pattern, response, re.IGNORECASE)
                if matches:
                    ygg_url = matches[0].rstrip('/')
                    # Validate URL format
                    if 'yggtorrent' in ygg_url.lower():
                        self._cache.save_url(ygg_url)
                        return ygg_url
        except Exception:
            pass  # Silently fall back
        
        # Return fallback URL
        return fallback_url


class yggapi:
    """
    YggAPI qBittorrent Search Plugin
    
    Provides search functionality for YggTorrent torrents via YggAPI
    with automatic URL discovery from yeeti.io
    """
    
    # qBittorrent plugin metadata
    name: str = "YggAPI"
    url: str = YggAPIConfig.API_BASE_URL
    supported_categories: Dict[str, str] = YggAPIConfig.CATEGORY_MAPPING
    
    def __init__(self):
        """Initialize the search plugin"""
        self._config = YggAPIConfig()
        self._current_page: int = 1
        self._max_page: int = 0  # 0 = unlimited
        self._per_page: int = self._config.DEFAULT_PER_PAGE
        self._order_by: str = self._config.DEFAULT_ORDER_BY
        
        # Initialize URL fetcher with cache
        cache = URLCache(
            self._config.URL_CACHE_FILE,
            self._config.URL_CACHE_DURATION_HOURS
        )
        url_fetcher = YggURLFetcher(self._config.YEETI_PROFILE_URL, cache)
        self._ygg_url: str = url_fetcher.get_ygg_url()
        
        # Passkey for torrent downloads
        self._passkey: str = self._config.PASSKEY
    
    def search(self, what: str, cat: str = "all") -> None:
        """
        Perform search and print results
        
        Args:
            what: Search query string
            cat: Category filter (all, movies, tv, music, games, anime, software, pictures, books)
        """
        self._current_page = 1
        
        while True:
            results = self._fetch_page(what, cat)
            
            if not results:
                break
            
            for torrent_data in results:
                self._print_result(torrent_data)
            
            # Check if we should fetch more pages
            if not self._should_continue_pagination(len(results)):
                break
            
            self._current_page += 1
    
    def _fetch_page(self, query: str, category: str) -> List[Dict[str, Any]]:
        """
        Fetch a single page of search results with retry logic
        
        Args:
            query: Search query string
            category: Category filter
            
        Returns:
            List of torrent dictionaries
        """
        search_url = self._build_search_url(query, category)
        
        for attempt in range(self._config.MAX_RETRIES):
            try:
                response = retrieve_url(search_url)
                results = json.loads(response)
                
                if isinstance(results, list):
                    return results
                else:
                    return []
                    
            except (json.JSONDecodeError, Exception) as e:
                if attempt < self._config.MAX_RETRIES - 1:
                    time.sleep(self._config.RETRY_DELAY_SECONDS)
                    continue
                else:
                    # Failed all retries
                    return []
        
        return []
    
    def _build_search_url(self, query: str, category: str) -> str:
        """
        Build the API search URL with parameters
        
        Args:
            query: Search query string
            category: Category filter (supports qBittorrent categories and extended categories)
            
        Returns:
            Complete search URL
        """
        params = {
            'q': query,
            'page': self._current_page,
            'per_page': self._per_page,
            'order_by': self._order_by
        }
        
        # Add category filter if specified
        if category != "all":
            category_id = self._resolve_category_id(category)
            if category_id:
                params['category_id'] = category_id
        
        return f"{self.url}/torrents?{urlencode(params)}"
    
    def _resolve_category_id(self, category: str) -> str:
        """
        Resolve category name to YggTorrent category ID
        
        Supports both qBittorrent standard categories and extended YggTorrent categories
        
        Args:
            category: Category name
            
        Returns:
            Category ID string or empty string if not found
        """
        # Try standard qBittorrent categories first
        if category in self.supported_categories:
            return self.supported_categories[category]
        
        # Try extended category mapping
        if category in self._config.EXTENDED_CATEGORY_MAPPING:
            return self._config.EXTENDED_CATEGORY_MAPPING[category]
        
        # Try direct category ID
        if category.isdigit() and category in self._config.YGG_CATEGORY_NAMES:
            return category
        
        return ""
    
    def _print_result(self, torrent: Dict[str, Any]) -> None:
        """
        Format and print a single torrent result
        
        Args:
            torrent: Torrent data dictionary from API
        """
        try:
            # Parse upload date
            pub_date = self._parse_date(torrent.get('uploaded_at', ''))
            
            # Build result dictionary for qBittorrent
            result = {
                "link": self._build_download_link(torrent.get('id', '')),
                "name": torrent.get('title', 'Unknown'),
                "size": self._parse_size(torrent.get('size', '-1')),
                "seeds": int(torrent.get('seeders', 0)),
                "leech": int(torrent.get('leechers', 0)),
                "engine_url": self.url,
                "desc_link": torrent.get('link', self._ygg_url),
                "pub_date": pub_date
            }
            
            prettyPrinter(result)
            
        except (KeyError, ValueError, TypeError):
            # Skip malformed results
            pass
    
    def _build_download_link(self, torrent_id: str) -> str:
        """
        Build torrent download link with passkey
        
        Args:
            torrent_id: Torrent ID from API
            
        Returns:
            Complete download URL
        """
        return f"{self.url}/torrent/{torrent_id}/download?passkey={self._passkey}"
    
    def _parse_date(self, date_string: str) -> int:
        """
        Parse ISO date string to Unix timestamp
        
        Args:
            date_string: ISO format date string
            
        Returns:
            Unix timestamp (seconds since epoch)
        """
        try:
            # Try parsing with timezone
            dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S%z")
            return int(dt.timestamp())
        except (ValueError, AttributeError):
            try:
                # Try without timezone
                dt = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
                return int(dt.timestamp())
            except (ValueError, AttributeError):
                # Return current time as fallback
                return int(time.time())
    
    def _parse_size(self, size: Any) -> str:
        """
        Ensure size is properly formatted as string
        
        Args:
            size: Size value (string or int)
            
        Returns:
            Size as string in bytes
        """
        if isinstance(size, int):
            return str(size)
        elif isinstance(size, str):
            return size
        else:
            return "-1"
    
    def _should_continue_pagination(self, results_count: int) -> bool:
        """
        Determine if pagination should continue
        
        Args:
            results_count: Number of results in current page
            
        Returns:
            True if more pages should be fetched
        """
        # Continue if we got a full page and haven't reached max_page limit
        has_more_results = results_count >= self._per_page
        within_page_limit = self._max_page <= 0 or self._current_page < self._max_page
        
        return has_more_results and within_page_limit
    
    @staticmethod
    def get_all_categories() -> Dict[str, Dict[str, str]]:
        """
        Get all available categories organized by type
        
        Returns:
            Dictionary of category groups with their mappings
        """
        return {
            "standard": YggAPIConfig.CATEGORY_MAPPING,
            "extended": YggAPIConfig.EXTENDED_CATEGORY_MAPPING,
            "ygg_names": YggAPIConfig.YGG_CATEGORY_NAMES
        }
    
    @staticmethod
    def get_category_count() -> int:
        """
        Get the total number of supported categories
        
        Returns:
            Total category count
        """
        return len(YggAPIConfig.YGG_CATEGORY_NAMES)
