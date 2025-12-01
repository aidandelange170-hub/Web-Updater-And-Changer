"""
Minimal web scraper for executable creation
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
import argparse

def scrape_url(url, timeout=10):
    """
    Scrape a single URL and extract content
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract title
        title = soup.title.string.strip() if soup.title else "No Title"
        
        # Extract text content
        text_content = soup.get_text()
        # Clean up text
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])
            link_text = link.get_text().strip()
            if link_text:
                links.append({"url": full_url, "text": link_text})
        
        # Extract images
        images = []
        for img in soup.find_all('img', src=True):
            full_url = urljoin(url, img['src'])
            alt_text = img.get('alt', '')
            images.append({"url": full_url, "alt": alt_text})
        
        return {
            "url": url,
            "title": title,
            "text_content": text_content[:5000],  # Limit content length
            "links": links,
            "images": images,
            "status_code": response.status_code
        }
    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "status_code": None
        }

def main():
    parser = argparse.ArgumentParser(description="Web Scraper Tool")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--output", "-o", default="output.json", help="Output file path")
    
    args = parser.parse_args()
    
    print(f"Scraping {args.url}...")
    result = scrape_url(args.url)
    
    # Save to file
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"Scraping completed. Results saved to {args.output}")
    print(f"Title: {result.get('title', 'N/A')}")
    print(f"Content length: {len(result.get('text_content', ''))} characters")

if __name__ == "__main__":
    main()