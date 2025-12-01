#!/usr/bin/env python3
"""
Web Scraper and Extractor powered by Google Search
This tool allows you to extract and scrape web content using Google search results
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import pandas as pd
from urllib.parse import urljoin, urlparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraper.log'),
        logging.StreamHandler()
    ]
)

class WebScraper:
    def __init__(self, use_selenium=False):  # Changed default to False for basic functionality
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.use_selenium = use_selenium
        self.driver = None
        
        if self.use_selenium:
            try:
                self.setup_selenium()
            except Exception as e:
                logging.warning(f"Selenium setup failed: {e}. Falling back to requests-based scraping.")
                self.use_selenium = False
    
    def setup_selenium(self):
        """Setup Selenium WebDriver with Chrome"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in background
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def google_search(self, query, num_results=10):
        """Perform Google search and return URLs"""
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}"
        
        if self.use_selenium:
            self.driver.get(search_url)
            time.sleep(2)  # Wait for page to load
            
            # Extract search result links
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "div.g a")
            urls = []
            for result in search_results[:num_results]:
                href = result.get_attribute('href')
                if href and 'http' in href:
                    urls.append(href)
            return urls
        else:
            # Fallback to requests-based approach (may be blocked)
            response = self.session.get(search_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('div', class_='g')
            urls = []
            for link in links[:num_results]:
                anchor = link.find('a')
                if anchor and anchor.get('href'):
                    urls.append(anchor.get('href'))
            return urls
    
    def scrape_page(self, url):
        """Scrape content from a single URL"""
        try:
            if self.use_selenium:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                html = self.driver.page_source
            else:
                response = self.session.get(url)
                html = response.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract content
            title = soup.find('title')
            title = title.text.strip() if title else "No Title"
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
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
                links.append({
                    'text': link.text.strip(),
                    'url': full_url
                })
            
            # Extract images
            images = []
            for img in soup.find_all('img', src=True):
                full_url = urljoin(url, img['src'])
                images.append({
                    'alt': img.get('alt', ''),
                    'src': full_url
                })
            
            return {
                'url': url,
                'title': title,
                'content': text_content,
                'links': links,
                'images': images,
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def scrape_multiple(self, urls):
        """Scrape multiple URLs"""
        results = []
        for i, url in enumerate(urls):
            logging.info(f"Scraping ({i+1}/{len(urls)}): {url}")
            result = self.scrape_page(url)
            results.append(result)
            
            # Be respectful - add delay between requests
            time.sleep(1)
        return results
    
    def search_and_scrape(self, query, num_results=5):
        """Search Google and scrape results"""
        logging.info(f"Searching Google for: {query}")
        urls = self.google_search(query, num_results)
        
        if not urls:
            logging.warning("No URLs found from Google search")
            return []
        
        logging.info(f"Found {len(urls)} URLs, starting to scrape...")
        results = self.scrape_multiple(urls)
        return results
    
    def save_results(self, results, filename=None):
        """Save scraping results to file"""
        if not filename:
            filename = f"data/scraping_results_{int(time.time())}.json"
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Also save as CSV if possible
        csv_filename = filename.replace('.json', '.csv')
        try:
            # Flatten the results for CSV
            flattened = []
            for result in results:
                flat_result = {
                    'url': result.get('url', ''),
                    'title': result.get('title', ''),
                    'content_preview': result.get('content', '')[:200] + '...' if result.get('content') else '',
                    'scraped_at': result.get('scraped_at', ''),
                    'error': result.get('error', ''),
                    'links_count': len(result.get('links', [])),
                    'images_count': len(result.get('images', []))
                }
                flattened.append(flat_result)
            
            df = pd.DataFrame(flattened)
            df.to_csv(csv_filename, index=False)
        except Exception as e:
            logging.error(f"Error saving CSV: {str(e)}")
        
        logging.info(f"Results saved to {filename} and {csv_filename}")
        return filename
    
    def close(self):
        """Close the scraper and clean up resources"""
        if self.driver:
            self.driver.quit()


def main():
    """Main function to run the scraper"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <search_query> [num_results]")
        print("Example: python main.py 'python web scraping' 5")
        sys.exit(1)
    
    query = sys.argv[1]
    num_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # Create directories if they don't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Initialize scraper
    scraper = WebScraper(use_selenium=True)
    
    try:
        # Search and scrape
        results = scraper.search_and_scrape(query, num_results)
        
        # Save results
        filename = scraper.save_results(results)
        
        # Print summary
        print(f"\nScraping completed!")
        print(f"Total URLs processed: {len(results)}")
        successful = sum(1 for r in results if 'error' not in r)
        print(f"Successful scrapes: {successful}")
        print(f"Results saved to: {filename}")
        
        # Show first few results
        print("\nFirst few results:")
        for i, result in enumerate(results[:3]):
            if 'error' not in result:
                print(f"{i+1}. {result['title'][:100]}...")
            else:
                print(f"{i+1}. Error: {result['error']}")
    
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
    finally:
        scraper.close()


if __name__ == "__main__":
    main()