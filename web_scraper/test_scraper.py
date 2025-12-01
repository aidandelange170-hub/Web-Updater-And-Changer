#!/usr/bin/env python3
"""
Test script for the web scraper functionality
"""

from main import WebScraper
import json
import os

def test_scraper():
    """Test the core scraping functionality"""
    print("Testing Web Scraper functionality...")
    
    # Create directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Test 1: Scrape a simple website
    print("\n1. Testing basic scraping functionality...")
    scraper = WebScraper(use_selenium=False)  # Use requests-based approach
    
    try:
        # Test scraping example.com
        result = scraper.scrape_page('https://example.com')
        
        if 'error' not in result:
            print(f"   Title: {result['title']}")
            print(f"   Content preview: {result['content'][:100]}...")
            print(f"   Found {len(result['links'])} links and {len(result['images'])} images")
            
            # Save result
            filename = scraper.save_results([result], 'data/test_result.json')
            print(f"   Result saved to {filename}")
        else:
            print(f"   Error: {result['error']}")
    
    finally:
        scraper.close()
    
    # Test 2: Scrape multiple URLs
    print("\n2. Testing multiple URL scraping...")
    scraper = WebScraper(use_selenium=False)
    
    test_urls = [
        'https://httpbin.org/html',
        'https://httpbin.org/json',
        'https://example.com'
    ]
    
    try:
        results = scraper.scrape_multiple(test_urls)
        
        for i, result in enumerate(results):
            if 'error' not in result:
                print(f"   {i+1}. {result['title'] or 'No Title'} - {len(result['content'])} chars")
            else:
                print(f"   {i+1}. Error: {result['error']}")
        
        # Save all results
        filename = scraper.save_results(results, 'data/multiple_test_results.json')
        print(f"   Results saved to {filename}")
        
    finally:
        scraper.close()
    
    # Test 3: Test with a more complex site (if accessible)
    print("\n3. Testing with a documentation site...")
    scraper = WebScraper(use_selenium=False)
    
    try:
        result = scraper.scrape_page('https://docs.python.org/3/')
        
        if 'error' not in result:
            print(f"   Title: {result['title']}")
            print(f"   Content length: {len(result['content'])} characters")
            print(f"   Links found: {len(result['links'])}")
            print(f"   Images found: {len(result['images'])}")
        else:
            print(f"   Error: {result['error']}")
            print("   This is expected for sites with anti-bot measures")
    
    finally:
        scraper.close()
    
    print("\nTesting completed!")

if __name__ == "__main__":
    test_scraper()