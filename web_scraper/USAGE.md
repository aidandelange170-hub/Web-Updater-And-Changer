# Web Scraper Usage Guide

## Overview
This web scraper is designed to extract content from websites using either requests-based scraping (default) or Selenium-based scraping for JavaScript-heavy sites.

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Basic Usage

### Command Line Interface
```bash
python main.py "search query" [number_of_results]
```

Example:
```bash
python main.py "python programming" 5
```

### Python API
```python
from main import WebScraper

# Initialize scraper (requests-based by default)
scraper = WebScraper(use_selenium=False)

# Scrape a single URL
result = scraper.scrape_page('https://example.com')
print(result['title'])
print(result['content'][:200])

# Scrape multiple URLs
urls = ['https://example.com', 'https://httpbin.org/html']
results = scraper.scrape_multiple(urls)

# Save results
scraper.save_results(results, 'my_results.json')

# Always close the scraper when done
scraper.close()
```

## Features

- **Content Extraction**: Extracts page titles, text content, links, and images
- **Multiple Output Formats**: Saves data in both JSON and CSV formats
- **Configurable Settings**: Customizable delays, user agents, and other settings
- **Error Handling**: Robust error handling with logging
- **Flexible Architecture**: Can switch between requests and Selenium backends

## Configuration

The scraper behavior can be customized via the `config/config.json` file:

```json
{
    "scraper_settings": {
        "use_selenium": false,
        "delay_between_requests": 1,
        "timeout": 10,
        "max_retries": 3,
        "user_agent": "Mozilla/5.0..."
    }
}
```

## Output Files

- **JSON files**: Detailed scraping results with full content
- **CSV files**: Summary data for analysis
- **Log files**: Detailed logs of scraping operations

## Limitations

- Google search functionality may be limited with requests-based approach due to anti-bot measures
- Some websites may block scraping attempts
- JavaScript-heavy sites work better with Selenium (requires Chrome installation)

## Legal Notice

Please use this tool responsibly and respect websites' `robots.txt` files and terms of service. Web scraping may be subject to legal restrictions in your jurisdiction.