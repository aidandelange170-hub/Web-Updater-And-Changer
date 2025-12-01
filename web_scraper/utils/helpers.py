"""
Utility functions for the web scraper
"""

import re
import time
import requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def validate_url(url):
    """Validate if a string is a proper URL"""
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url) is not None


def get_domain(url):
    """Extract domain from URL"""
    parsed = urlparse(url)
    return parsed.netloc


def check_url_reachable(url, timeout=10):
    """Check if a URL is reachable"""
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except:
        return False


def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def wait_random(min_time=1, max_time=3):
    """Wait for a random amount of time"""
    import random
    wait_time = random.uniform(min_time, max_time)
    time.sleep(wait_time)


def setup_chrome_driver(headless=True):
    """Setup Chrome WebDriver with recommended options"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    return webdriver.Chrome(options=chrome_options)


def extract_emails(text):
    """Extract email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)


def extract_phone_numbers(text):
    """Extract phone numbers from text"""
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    return re.findall(phone_pattern, text)