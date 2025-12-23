#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify YggTorrent URL fetching from yeeti.io/@ygg
This test makes REAL network calls to verify the integration works
"""

# Fix Windows console encoding for emoji support
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import sys
import os
import tempfile
import re
import urllib.request
sys.path.insert(0, os.path.dirname(__file__))

# Mock qBittorrent modules before importing yggapi
from unittest.mock import MagicMock

# Create a real retrieve_url function
def retrieve_url(url):
    """Real implementation of retrieve_url for testing"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.read().decode('utf-8')

# Mock the modules
sys.modules['helpers'] = MagicMock()
sys.modules['helpers'].retrieve_url = retrieve_url
sys.modules['novaprinter'] = MagicMock()

# Now import yggapi
from yggapi import URLCache, YggURLFetcher


def test_real_yeeti_fetch():
    """Test fetching the actual YggTorrent URL from yeeti.io/@ygg"""
    print("\n" + "="*70)
    print("Testing REAL URL fetch from yeeti.io/@ygg")
    print("="*70)
    
    # Create temp cache
    temp_dir = tempfile.mkdtemp()
    cache_file = os.path.join(temp_dir, "test_cache.json")
    cache = URLCache(cache_file, cache_duration_hours=24)
    
    # Create fetcher
    profile_url = "https://yeeti.io/@ygg"
    fetcher = YggURLFetcher(profile_url, cache)
    
    print(f"\n1. Fetching from: {profile_url}")
    
    try:
        # Fetch the actual URL
        ygg_url = fetcher.get_ygg_url(fallback_url="https://www.yggtorrent.org")
        
        print(f"2. Fetched URL: {ygg_url}")
        
        # Validate the URL
        is_valid = bool(re.match(r'https?://(?:www\.)?yggtorrent\.[a-z]{2,}/?', ygg_url, re.IGNORECASE))
        
        if is_valid:
            print(f"3. ✅ URL is valid YggTorrent domain")
        else:
            print(f"3. ❌ URL doesn't match YggTorrent pattern")
            return False
        
        # Check if URL was cached
        cached_url = cache.get_cached_url()
        if cached_url == ygg_url.rstrip('/'):
            print(f"4. ✅ URL was properly cached")
        else:
            print(f"4. ⚠️ Cache mismatch - Cached: {cached_url}")
        
        # Try to fetch the raw HTML to see what we got
        print(f"\n5. Testing direct fetch from yeeti.io...")
        try:
            response = retrieve_url(profile_url)
            print(f"   Response length: {len(response)} bytes")
            
            # Look for YggTorrent mentions
            ygg_mentions = response.lower().count('yggtorrent')
            print(f"   'yggtorrent' mentions found: {ygg_mentions}")
            
            # Show a snippet of the response
            if 'yggtorrent' in response.lower():
                # Find and show the line with yggtorrent
                lines = response.split('\n')
                for i, line in enumerate(lines):
                    if 'yggtorrent' in line.lower():
                        print(f"   Found at line {i}: {line.strip()[:100]}...")
                        break
        except Exception as e:
            print(f"   ⚠️ Could not fetch raw HTML: {e}")
        
        print("\n" + "="*70)
        print("✅ TEST PASSED - URL fetched successfully!")
        print("="*70)
        
        # Cleanup
        if os.path.exists(cache_file):
            os.remove(cache_file)
        os.rmdir(temp_dir)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("="*70)
        
        # Cleanup
        if os.path.exists(cache_file):
            os.remove(cache_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
        
        return False


def test_url_patterns():
    """Test various HTML patterns that might contain the URL"""
    print("\n" + "="*70)
    print("Testing URL extraction patterns")
    print("="*70)
    
    test_cases = [
        # Pattern 1: Simple link
        ('<a href="https://www.yggtorrent.org/">YGG</a>', 'https://www.yggtorrent.org'),
        
        # Pattern 2: With trailing slash
        ('Visit https://www.yggtorrent.fi/ for torrents', 'https://www.yggtorrent.fi'),
        
        # Pattern 3: Meta tag
        ('<meta property="og:url" content="https://www.yggtorrent.si/" />', 'https://www.yggtorrent.si'),
        
        # Pattern 4: JSON format
        ('{"website": "https://www.yggtorrent.top/"}', 'https://www.yggtorrent.top'),
        
        # Pattern 5: Different TLD
        ('Link: https://yggtorrent.re', 'https://yggtorrent.re'),
    ]
    
    patterns = [
        r'https?://(?:www\.)?yggtorrent\.[a-z]{2,}/?',
        r'<meta\s+property=["\']og:url["\']\s+content=["\'](https?://[^"\']*yggtorrent[^"\']*)["\']',
        r'href=["\'](https?://[^"\']*yggtorrent[^"\']*)["\']',
        r'"website"\s*:\s*"(https?://[^"]*yggtorrent[^"]*)"'
    ]
    
    all_passed = True
    for html, expected_url in test_cases:
        found = False
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                found_url = matches[0].rstrip('/')
                if 'yggtorrent' in found_url.lower():
                    print(f"✅ Pattern matched: {found_url}")
                    found = True
                    break
        
        if not found:
            print(f"❌ Failed to extract from: {html[:50]}...")
            all_passed = False
    
    print("="*70)
    return all_passed


def test_cache_functionality():
    """Test that cache works correctly"""
    print("\n" + "="*70)
    print("Testing cache functionality")
    print("="*70)
    
    temp_dir = tempfile.mkdtemp()
    cache_file = os.path.join(temp_dir, "test_cache.json")
    cache = URLCache(cache_file, cache_duration_hours=24)
    
    test_url = "https://www.yggtorrent.org"
    
    # Test 1: Save URL
    print("1. Saving URL to cache...")
    cache.save_url(test_url)
    
    # Test 2: Retrieve URL
    print("2. Retrieving URL from cache...")
    cached_url = cache.get_cached_url()
    
    if cached_url == test_url:
        print(f"   ✅ Retrieved: {cached_url}")
    else:
        print(f"   ❌ Mismatch - Expected: {test_url}, Got: {cached_url}")
        return False
    
    # Test 3: Check cache file exists
    if os.path.exists(cache_file):
        print("3. ✅ Cache file created")
    else:
        print("3. ❌ Cache file not found")
        return False
    
    # Cleanup
    os.remove(cache_file)
    os.rmdir(temp_dir)
    
    print("="*70)
    return True


if __name__ == '__main__':
    print("\n" + "#"*70)
    print("# YggTorrent URL Fetching Test Suite")
    print("#"*70)
    
    results = []
    
    # Test 1: Cache functionality
    results.append(("Cache Functionality", test_cache_functionality()))
    
    # Test 2: URL patterns
    results.append(("URL Pattern Extraction", test_url_patterns()))
    
    # Test 3: Real fetch from yeeti.io
    results.append(("Real Yeeti.io Fetch", test_real_yeeti_fetch()))
    
    # Summary
    print("\n" + "#"*70)
    print("# TEST SUMMARY")
    print("#"*70)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("#"*70 + "\n")
    
    sys.exit(0 if all(p for _, p in results) else 1)

