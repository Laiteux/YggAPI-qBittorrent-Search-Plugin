#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YggAPI qBittorrent Search Plugin - Test Suite

Comprehensive unit tests for all YggAPI components following best practices:
- Isolated tests with no external dependencies
- Mocked network calls and file I/O
- Clear test naming and organization
- Edge case and error condition coverage
- DRY principle with helper methods
- SOLID principles adherence

Run tests:
    python -m unittest test_yggapi.py
    python -m unittest test_yggapi.py -v  # Verbose output
    python -m unittest test_yggapi.TestURLCache  # Run specific test class
"""

import json
import os
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open, call
from typing import Dict, Any


# Import the module under test
# Note: In real environment, this would import from yggapi
# For testing, we'll need to mock the external dependencies
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Mock the qBittorrent-provided modules before importing yggapi
sys.modules['helpers'] = MagicMock()
sys.modules['novaprinter'] = MagicMock()

from yggapi import (
    YggAPIConfig,
    URLCache,
    YggURLFetcher,
    yggapi
)


class TestYggAPIConfig(unittest.TestCase):
    """Test suite for YggAPIConfig class"""
    
    def test_api_base_url_is_defined(self):
        """Test that API base URL is properly defined"""
        self.assertEqual(YggAPIConfig.API_BASE_URL, "https://yggapi.eu")
        self.assertIsInstance(YggAPIConfig.API_BASE_URL, str)
    
    def test_passkey_has_default_value(self):
        """Test that PASSKEY has a default placeholder value"""
        self.assertIsInstance(YggAPIConfig.PASSKEY, str)
        self.assertGreater(len(YggAPIConfig.PASSKEY), 0)
    
    def test_yeeti_profile_url_is_correct(self):
        """Test that Yeeti.io profile URL is correctly configured"""
        self.assertEqual(YggAPIConfig.YEETI_PROFILE_URL, "https://yeeti.io/@ygg")
    
    def test_cache_duration_is_positive(self):
        """Test that cache duration is a positive integer"""
        self.assertIsInstance(YggAPIConfig.URL_CACHE_DURATION_HOURS, int)
        self.assertGreater(YggAPIConfig.URL_CACHE_DURATION_HOURS, 0)
    
    def test_default_per_page_is_reasonable(self):
        """Test that default per_page value is reasonable"""
        self.assertIsInstance(YggAPIConfig.DEFAULT_PER_PAGE, int)
        self.assertGreater(YggAPIConfig.DEFAULT_PER_PAGE, 0)
        self.assertLessEqual(YggAPIConfig.DEFAULT_PER_PAGE, 1000)
    
    def test_max_retries_is_positive(self):
        """Test that max retries is a positive integer"""
        self.assertIsInstance(YggAPIConfig.MAX_RETRIES, int)
        self.assertGreater(YggAPIConfig.MAX_RETRIES, 0)
    
    def test_category_mapping_structure(self):
        """Test that category mapping has correct structure"""
        self.assertIsInstance(YggAPIConfig.CATEGORY_MAPPING, dict)
        self.assertIn("all", YggAPIConfig.CATEGORY_MAPPING)
        self.assertIn("movies", YggAPIConfig.CATEGORY_MAPPING)
        self.assertIn("tv", YggAPIConfig.CATEGORY_MAPPING)
        
        # Test all values are strings
        for key, value in YggAPIConfig.CATEGORY_MAPPING.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, str)
    
    def test_ygg_category_names_structure(self):
        """Test that YGG category names have correct structure"""
        self.assertIsInstance(YggAPIConfig.YGG_CATEGORY_NAMES, dict)
        self.assertGreater(len(YggAPIConfig.YGG_CATEGORY_NAMES), 50)
        
        # Test specific categories
        self.assertIn("2183", YggAPIConfig.YGG_CATEGORY_NAMES)  # Film
        self.assertIn("2184", YggAPIConfig.YGG_CATEGORY_NAMES)  # Série TV
        
        # Test all values are strings
        for key, value in YggAPIConfig.YGG_CATEGORY_NAMES.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, str)
    
    def test_extended_category_mapping_structure(self):
        """Test that extended category mapping has correct structure"""
        self.assertIsInstance(YggAPIConfig.EXTENDED_CATEGORY_MAPPING, dict)
        self.assertIn("animation", YggAPIConfig.EXTENDED_CATEGORY_MAPPING)
        self.assertIn("manga", YggAPIConfig.EXTENDED_CATEGORY_MAPPING)
        
        # Test values are valid category IDs
        for key, value in YggAPIConfig.EXTENDED_CATEGORY_MAPPING.items():
            self.assertIsInstance(value, str)
            self.assertTrue(value.isdigit())


class TestURLCache(unittest.TestCase):
    """Test suite for URLCache class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "test_cache.json")
        self.cache = URLCache(self.cache_file, cache_duration_hours=24)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove test cache file if it exists
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        os.rmdir(self.temp_dir)
    
    def test_cache_initialization(self):
        """Test that cache initializes correctly"""
        self.assertIsInstance(self.cache, URLCache)
        self.assertEqual(self.cache._cache_file, Path(self.cache_file))
        self.assertEqual(self.cache._cache_duration, timedelta(hours=24))
    
    def test_get_cached_url_when_no_cache_exists(self):
        """Test getting cached URL when cache file doesn't exist"""
        result = self.cache.get_cached_url()
        self.assertIsNone(result)
    
    def test_save_and_retrieve_url(self):
        """Test saving and retrieving a URL from cache"""
        test_url = "https://www.yggtorrent.org"
        
        # Save URL
        self.cache.save_url(test_url)
        
        # Retrieve URL
        cached_url = self.cache.get_cached_url()
        self.assertEqual(cached_url, test_url)
    
    def test_cache_file_structure(self):
        """Test that cache file has correct JSON structure"""
        test_url = "https://www.yggtorrent.org"
        self.cache.save_url(test_url)
        
        with open(self.cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        self.assertIn('url', cache_data)
        self.assertIn('timestamp', cache_data)
        self.assertEqual(cache_data['url'], test_url)
        
        # Verify timestamp is valid ISO format
        datetime.fromisoformat(cache_data['timestamp'])
    
    def test_expired_cache_returns_none(self):
        """Test that expired cache returns None"""
        test_url = "https://www.yggtorrent.org"
        
        # Create cache with expired timestamp
        expired_time = datetime.now() - timedelta(hours=25)
        cache_data = {
            'url': test_url,
            'timestamp': expired_time.isoformat()
        }
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f)
        
        # Should return None because cache is expired
        result = self.cache.get_cached_url()
        self.assertIsNone(result)
    
    def test_invalid_json_returns_none(self):
        """Test that invalid JSON in cache file returns None"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            f.write("invalid json content")
        
        result = self.cache.get_cached_url()
        self.assertIsNone(result)
    
    def test_cache_with_missing_fields_returns_none(self):
        """Test that cache with missing fields returns None"""
        # Cache with missing URL
        cache_data = {'timestamp': datetime.now().isoformat()}
        
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f)
        
        result = self.cache.get_cached_url()
        self.assertIsNone(result)
    
    def test_save_url_with_io_error_fails_gracefully(self):
        """Test that save_url fails gracefully on I/O error"""
        # Use invalid path to trigger I/O error
        invalid_cache = URLCache("/invalid/path/cache.json", 24)
        
        # Should not raise exception
        try:
            invalid_cache.save_url("https://test.com")
        except Exception as e:
            self.fail(f"save_url raised {type(e).__name__} unexpectedly")


class TestYggURLFetcher(unittest.TestCase):
    """Test suite for YggURLFetcher class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_file = os.path.join(self.temp_dir, "test_cache.json")
        self.cache = URLCache(self.cache_file, cache_duration_hours=24)
        self.profile_url = "https://yeeti.io/@ygg"
        self.fetcher = YggURLFetcher(self.profile_url, self.cache)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        os.rmdir(self.temp_dir)
    
    def test_fetcher_initialization(self):
        """Test that URL fetcher initializes correctly"""
        self.assertIsInstance(self.fetcher, YggURLFetcher)
        self.assertEqual(self.fetcher._profile_url, self.profile_url)
        self.assertEqual(self.fetcher._cache, self.cache)
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_from_profile_html(self, mock_retrieve):
        """Test extracting YggTorrent URL from profile HTML"""
        # Mock HTML response with YggTorrent URL
        mock_html = """
        <html>
        <body>
            <div class="bio">
                <a href="https://www.yggtorrent.org/">YggTorrent</a>
            </div>
        </body>
        </html>
        """
        mock_retrieve.return_value = mock_html
        
        result = self.fetcher.get_ygg_url()
        
        self.assertEqual(result, "https://www.yggtorrent.org")
        mock_retrieve.assert_called_once_with(self.profile_url)
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_from_meta_tag(self, mock_retrieve):
        """Test extracting YggTorrent URL from meta tag"""
        mock_html = """
        <html>
        <head>
            <meta property="og:url" content="https://www.yggtorrent.fi/" />
        </head>
        </html>
        """
        mock_retrieve.return_value = mock_html
        
        result = self.fetcher.get_ygg_url()
        
        self.assertEqual(result, "https://www.yggtorrent.fi")
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_from_json(self, mock_retrieve):
        """Test extracting YggTorrent URL from JSON data"""
        mock_json = '{"website": "https://www.yggtorrent.si/"}'
        mock_retrieve.return_value = mock_json
        
        result = self.fetcher.get_ygg_url()
        
        self.assertEqual(result, "https://www.yggtorrent.si")
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_strips_trailing_slash(self, mock_retrieve):
        """Test that trailing slash is removed from URL"""
        mock_html = '<a href="https://www.yggtorrent.org/">Link</a>'
        mock_retrieve.return_value = mock_html
        
        result = self.fetcher.get_ygg_url()
        
        self.assertEqual(result, "https://www.yggtorrent.org")
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_returns_fallback_on_error(self, mock_retrieve):
        """Test that fallback URL is returned on error"""
        mock_retrieve.side_effect = Exception("Network error")
        
        fallback = "https://www.yggtorrent.org"
        result = self.fetcher.get_ygg_url(fallback_url=fallback)
        
        self.assertEqual(result, fallback)
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_returns_fallback_when_no_url_found(self, mock_retrieve):
        """Test that fallback URL is returned when no YggTorrent URL found"""
        mock_html = "<html><body>No YggTorrent link here</body></html>"
        mock_retrieve.return_value = mock_html
        
        fallback = "https://www.yggtorrent.org"
        result = self.fetcher.get_ygg_url(fallback_url=fallback)
        
        self.assertEqual(result, fallback)
    
    def test_get_ygg_url_uses_cache_when_available(self):
        """Test that cached URL is used when available"""
        # Save URL to cache
        cached_url = "https://www.yggtorrent.cached"
        self.cache.save_url(cached_url)
        
        # Should return cached URL without making network call
        with patch('yggapi.retrieve_url') as mock_retrieve:
            result = self.fetcher.get_ygg_url()
            
            self.assertEqual(result, cached_url)
            mock_retrieve.assert_not_called()
    
    @patch('yggapi.retrieve_url')
    def test_get_ygg_url_caches_successful_fetch(self, mock_retrieve):
        """Test that successfully fetched URL is cached"""
        mock_html = '<a href="https://www.yggtorrent.fi/">Link</a>'
        mock_retrieve.return_value = mock_html
        
        result = self.fetcher.get_ygg_url()
        
        # Verify URL was cached
        cached_url = self.cache.get_cached_url()
        self.assertEqual(cached_url, result)


class TestYggapiMainClass(unittest.TestCase):
    """Test suite for main yggapi search class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the qBittorrent modules
        self.mock_retrieve_url = patch('yggapi.retrieve_url').start()
        self.mock_pretty_printer = patch('yggapi.prettyPrinter').start()
        
        # Create instance
        with patch.object(YggURLFetcher, 'get_ygg_url', return_value='https://www.yggtorrent.org'):
            self.plugin = yggapi()
    
    def tearDown(self):
        """Clean up test fixtures"""
        patch.stopall()
    
    def test_plugin_initialization(self):
        """Test that plugin initializes correctly"""
        self.assertIsInstance(self.plugin, yggapi)
        self.assertEqual(self.plugin.name, "YggAPI")
        self.assertEqual(self.plugin.url, "https://yggapi.eu")
        self.assertIsInstance(self.plugin.supported_categories, dict)
    
    def test_initial_page_is_one(self):
        """Test that initial page number is 1"""
        self.assertEqual(self.plugin._current_page, 1)
    
    def test_default_per_page_value(self):
        """Test that default per_page is set correctly"""
        self.assertEqual(self.plugin._per_page, 100)
    
    def test_default_order_by_is_seeders(self):
        """Test that default order_by is seeders"""
        self.assertEqual(self.plugin._order_by, "seeders")
    
    def test_ygg_url_is_fetched(self):
        """Test that YggTorrent URL is fetched during initialization"""
        self.assertIsNotNone(self.plugin._ygg_url)
        self.assertIsInstance(self.plugin._ygg_url, str)
    
    def test_build_search_url_with_query_only(self):
        """Test building search URL with query only"""
        url = self.plugin._build_search_url("test query", "all")
        
        self.assertIn("https://yggapi.eu/torrents", url)
        self.assertIn("q=test+query", url)
        self.assertIn("page=1", url)
        self.assertIn("per_page=100", url)
        self.assertIn("order_by=seeders", url)
    
    def test_build_search_url_with_category(self):
        """Test building search URL with category filter"""
        url = self.plugin._build_search_url("test", "movies")
        
        self.assertIn("category_id=2183", url)
    
    def test_build_search_url_with_invalid_category(self):
        """Test building search URL with invalid category"""
        url = self.plugin._build_search_url("test", "invalid_category")
        
        self.assertNotIn("category_id", url)
    
    def test_resolve_category_id_standard(self):
        """Test resolving standard qBittorrent category"""
        category_id = self.plugin._resolve_category_id("movies")
        self.assertEqual(category_id, "2183")
    
    def test_resolve_category_id_extended(self):
        """Test resolving extended category"""
        category_id = self.plugin._resolve_category_id("manga")
        self.assertEqual(category_id, "2155")
    
    def test_resolve_category_id_direct(self):
        """Test resolving direct category ID"""
        category_id = self.plugin._resolve_category_id("2183")
        self.assertEqual(category_id, "2183")
    
    def test_resolve_category_id_invalid(self):
        """Test resolving invalid category returns empty string"""
        category_id = self.plugin._resolve_category_id("invalid")
        self.assertEqual(category_id, "")
    
    def test_parse_date_with_timezone(self):
        """Test parsing ISO date with timezone"""
        date_string = "2024-01-15T14:30:00+01:00"
        timestamp = self.plugin._parse_date(date_string)
        
        self.assertIsInstance(timestamp, int)
        self.assertGreater(timestamp, 0)
    
    def test_parse_date_without_timezone(self):
        """Test parsing ISO date without timezone"""
        date_string = "2024-01-15T14:30:00"
        timestamp = self.plugin._parse_date(date_string)
        
        self.assertIsInstance(timestamp, int)
        self.assertGreater(timestamp, 0)
    
    def test_parse_date_invalid_returns_current_time(self):
        """Test that invalid date returns current timestamp"""
        invalid_date = "invalid-date"
        timestamp = self.plugin._parse_date(invalid_date)
        
        current_time = int(time.time())
        self.assertIsInstance(timestamp, int)
        # Should be within 1 second of current time
        self.assertAlmostEqual(timestamp, current_time, delta=1)
    
    def test_parse_size_integer(self):
        """Test parsing size as integer"""
        size = self.plugin._parse_size(1234567890)
        self.assertEqual(size, "1234567890")
    
    def test_parse_size_string(self):
        """Test parsing size as string"""
        size = self.plugin._parse_size("1234567890")
        self.assertEqual(size, "1234567890")
    
    def test_parse_size_invalid_returns_negative_one(self):
        """Test that invalid size returns -1"""
        size = self.plugin._parse_size(None)
        self.assertEqual(size, "-1")
    
    def test_should_continue_pagination_with_full_page(self):
        """Test pagination continues with full page of results"""
        self.plugin._per_page = 100
        self.plugin._max_page = 0
        
        should_continue = self.plugin._should_continue_pagination(100)
        self.assertTrue(should_continue)
    
    def test_should_continue_pagination_with_partial_page(self):
        """Test pagination stops with partial page of results"""
        self.plugin._per_page = 100
        
        should_continue = self.plugin._should_continue_pagination(50)
        self.assertFalse(should_continue)
    
    def test_should_continue_pagination_respects_max_page(self):
        """Test pagination stops when max_page is reached"""
        self.plugin._per_page = 100
        self.plugin._max_page = 2
        self.plugin._current_page = 2
        
        should_continue = self.plugin._should_continue_pagination(100)
        self.assertFalse(should_continue)
    
    def test_fetch_page_success(self):
        """Test successful page fetch"""
        mock_results = [
            {"id": "1", "title": "Test 1", "seeders": 10, "leechers": 5},
            {"id": "2", "title": "Test 2", "seeders": 20, "leechers": 10}
        ]
        self.mock_retrieve_url.return_value = json.dumps(mock_results)
        
        results = self.plugin._fetch_page("test query", "all")
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "Test 1")
    
    def test_fetch_page_with_json_error(self):
        """Test page fetch with JSON decode error"""
        self.mock_retrieve_url.return_value = "invalid json"
        
        results = self.plugin._fetch_page("test query", "all")
        
        self.assertEqual(results, [])
    
    def test_fetch_page_with_network_error_retries(self):
        """Test that page fetch retries on network error"""
        self.mock_retrieve_url.side_effect = Exception("Network error")
        
        results = self.plugin._fetch_page("test query", "all")
        
        # Should have retried MAX_RETRIES times
        self.assertEqual(self.mock_retrieve_url.call_count, 3)
        self.assertEqual(results, [])
    
    def test_print_result_with_valid_data(self):
        """Test printing result with valid torrent data"""
        torrent = {
            "id": "12345",
            "title": "Test Torrent",
            "size": "1234567890",
            "seeders": 100,
            "leechers": 50,
            "link": "https://www.yggtorrent.org/torrent/12345",
            "uploaded_at": "2024-01-15T14:30:00+01:00"
        }
        
        self.plugin._print_result(torrent)
        
        # Verify prettyPrinter was called
        self.mock_pretty_printer.assert_called_once()
        
        # Verify result structure
        call_args = self.mock_pretty_printer.call_args[0][0]
        self.assertIn("link", call_args)
        self.assertIn("name", call_args)
        self.assertIn("size", call_args)
        self.assertIn("seeds", call_args)
        self.assertIn("leech", call_args)
    
    def test_print_result_with_malformed_data_fails_gracefully(self):
        """Test that malformed torrent data fails gracefully"""
        malformed_torrent = {"incomplete": "data"}
        
        # Should not raise exception
        try:
            self.plugin._print_result(malformed_torrent)
        except Exception as e:
            self.fail(f"_print_result raised {type(e).__name__} unexpectedly")
    
    def test_build_download_link(self):
        """Test building download link with passkey"""
        torrent_id = "12345"
        link = self.plugin._build_download_link(torrent_id)
        
        self.assertIn("https://yggapi.eu/torrent/12345/download", link)
        self.assertIn("passkey=", link)
    
    def test_get_all_categories(self):
        """Test getting all categories"""
        categories = yggapi.get_all_categories()
        
        self.assertIsInstance(categories, dict)
        self.assertIn("standard", categories)
        self.assertIn("extended", categories)
        self.assertIn("ygg_names", categories)
    
    def test_get_category_count(self):
        """Test getting category count"""
        count = yggapi.get_category_count()
        
        self.assertIsInstance(count, int)
        self.assertGreater(count, 50)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete search workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_retrieve_url = patch('yggapi.retrieve_url').start()
        self.mock_pretty_printer = patch('yggapi.prettyPrinter').start()
        
        with patch.object(YggURLFetcher, 'get_ygg_url', return_value='https://www.yggtorrent.org'):
            self.plugin = yggapi()
    
    def tearDown(self):
        """Clean up test fixtures"""
        patch.stopall()
    
    def test_complete_search_workflow_single_page(self):
        """Test complete search workflow with single page of results"""
        mock_results = [
            {
                "id": "1",
                "title": "Test Movie 1",
                "size": "1234567890",
                "seeders": 100,
                "leechers": 50,
                "link": "https://www.yggtorrent.org/torrent/1",
                "uploaded_at": "2024-01-15T14:30:00+01:00"
            }
        ]
        self.mock_retrieve_url.return_value = json.dumps(mock_results)
        
        self.plugin.search("test query", "movies")
        
        # Verify search was executed
        self.mock_retrieve_url.assert_called()
        self.mock_pretty_printer.assert_called()
    
    def test_complete_search_workflow_multiple_pages(self):
        """Test complete search workflow with multiple pages"""
        # Mock first page with full results
        first_page = [{"id": str(i), "title": f"Movie {i}", "size": "100",
                      "seeders": 10, "leechers": 5, 
                      "link": f"https://ygg.org/{i}",
                      "uploaded_at": "2024-01-15T14:30:00+01:00"}
                     for i in range(100)]
        
        # Mock second page with partial results
        second_page = [{"id": "101", "title": "Movie 101", "size": "100",
                       "seeders": 10, "leechers": 5,
                       "link": "https://ygg.org/101",
                       "uploaded_at": "2024-01-15T14:30:00+01:00"}]
        
        self.mock_retrieve_url.side_effect = [
            json.dumps(first_page),
            json.dumps(second_page)
        ]
        
        self.plugin.search("test query", "all")
        
        # Verify both pages were fetched
        self.assertEqual(self.mock_retrieve_url.call_count, 2)
        # Verify all results were printed (100 + 1)
        self.assertEqual(self.mock_pretty_printer.call_count, 101)
    
    def test_search_with_no_results(self):
        """Test search that returns no results"""
        self.mock_retrieve_url.return_value = json.dumps([])
        
        self.plugin.search("nonexistent query", "all")
        
        # Verify search was attempted
        self.mock_retrieve_url.assert_called_once()
        # Verify no results were printed
        self.mock_pretty_printer.assert_not_called()


class TestEdgeCases(unittest.TestCase):
    """Test suite for edge cases and error conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        patch('yggapi.retrieve_url').start()
        patch('yggapi.prettyPrinter').start()
        
        with patch.object(YggURLFetcher, 'get_ygg_url', return_value='https://www.yggtorrent.org'):
            self.plugin = yggapi()
    
    def tearDown(self):
        """Clean up test fixtures"""
        patch.stopall()
    
    def test_search_with_empty_query(self):
        """Test search with empty query string"""
        url = self.plugin._build_search_url("", "all")
        self.assertIn("q=", url)
    
    def test_search_with_special_characters(self):
        """Test search with special characters in query"""
        url = self.plugin._build_search_url("test & special / chars", "all")
        self.assertIn("q=", url)
    
    def test_parse_date_with_empty_string(self):
        """Test parsing empty date string"""
        timestamp = self.plugin._parse_date("")
        self.assertIsInstance(timestamp, int)
    
    def test_parse_size_with_zero(self):
        """Test parsing size with zero value"""
        size = self.plugin._parse_size(0)
        self.assertEqual(size, "0")
    
    def test_resolve_category_with_empty_string(self):
        """Test resolving category with empty string"""
        category_id = self.plugin._resolve_category_id("")
        self.assertEqual(category_id, "")
    
    def test_should_continue_pagination_with_zero_results(self):
        """Test pagination with zero results"""
        should_continue = self.plugin._should_continue_pagination(0)
        self.assertFalse(should_continue)


def run_test_suite():
    """Run the complete test suite with detailed output"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestYggAPIConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestURLCache))
    suite.addTests(loader.loadTestsFromTestCase(TestYggURLFetcher))
    suite.addTests(loader.loadTestsFromTestCase(TestYggapiMainClass))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run the test suite
    success = run_test_suite()
    sys.exit(0 if success else 1)

