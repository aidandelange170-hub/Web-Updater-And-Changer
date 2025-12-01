#!/usr/bin/env python3
"""
Example usage of the Web Scraper
"""

from main import WebScraper
import json

def example_search_and_scrape():
    """Example: Search and scrape"""
    print("Starting web scraper example...")
    
    # Initialize scraper with requests-based approach (selenium=False)
    scraper = WebScraper(use_selenium=False)
    
    try:
        # Example 1: Search and scrape
        print("\n1. Searching Google for 'openai' and scraping results...")
        results = scraper.search_and_scrape('openai', num_results=3)
        
        print(f"Retrieved {len(results)} results")
        
        # Print summary of results
        for i, result in enumerate(results):
            if 'error' not in result:
                print(f"  {i+1}. {result['title']}")
                print(f"     Content length: {len(result['content'])} characters")
                print(f"     Links found: {len(result['links'])}")
                print(f"     Images found: {len(result['images'])}")
            else:
                print(f"  {i+1}. Error: {result['error']}")
        
        # Save results
        filename = scraper.save_results(results, 'data/example_results.json')
        print(f"\nResults saved to {filename}")
        
        # Example 2: Scrape specific URLs
        print("\n2. Scraping specific URLs...")
        specific_urls = [
            'https://httpbin.org/html',  # Test page
            'https://httpbin.org/json'   # Test page
        ]
        
        specific_results = scraper.scrape_multiple(specific_urls)
        for result in specific_results:
            if 'error' not in result:
                print(f"  Scraped: {result['title'][:50]}...")
            else:
                print(f"  Error scraping: {result['error']}")
        
        # Save specific results
        scraper.save_results(specific_results, 'data/specific_results.json')
        
    finally:
        scraper.close()
        print("\nScraper closed.")

def example_direct_scraping():
    """Example: Direct scraping of a URL"""
    scraper = WebScraper(use_selenium=False)
    
    try:
        print("\n3. Direct scraping example...")
        result = scraper.scrape_page('https://example.com')
        
        if 'error' not in result:
            print(f"Title: {result['title']}")
            print(f"Content preview: {result['content'][:200]}...")
            print(f"Found {len(result['links'])} links and {len(result['images'])} images")
        else:
            print(f"Error: {result['error']}")
    finally:
        scraper.close()

if __name__ == "__main__":
    example_search_and_scrape()
    example_direct_scraping()
    print("\nExamples completed!")