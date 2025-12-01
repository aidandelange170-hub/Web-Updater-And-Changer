# Web Scraper and Extractor

A powerful web scraping tool powered by Google Search that allows you to extract and scrape web content automatically.

## Features

- Google search integration to find relevant URLs
- Advanced web scraping using Selenium and BeautifulSoup
- Support for JavaScript-heavy websites
- Data extraction (text, links, images, emails, phone numbers)
- Multiple output formats (JSON, CSV)
- Configurable settings
- Logging and error handling

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py "search query" [number_of_results]
```

Example:
```bash
python main.py "python web scraping" 5
```

### Advanced Usage

You can also run individual components:

```bash
# Scrape a specific URL
python -c "from main import WebScraper; s = WebScraper(); result = s.scrape_page('https://example.com'); print(result['title'])"
```

## Configuration

The scraper can be configured using the `config/config.json` file:

- `scraper_settings`: Configure scraping behavior
- `output_settings`: Configure output format and locations
- `google_settings`: Configure Google search parameters

## Project Structure

```
web_scraper/
├── main.py                 # Main scraper application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── config/                # Configuration files
│   └── config.json        # Main configuration
├── scraper/               # Scraper modules (future)
├── utils/                 # Utility functions
│   └── helpers.py         # Helper functions
├── data/                  # Output data files
└── logs/                  # Log files
```

## Output

The scraper generates:

- JSON files with detailed scraping results
- CSV files with summary information
- Log files for debugging

## Legal Notice

Please use this tool responsibly and respect websites' `robots.txt` files and terms of service. Web scraping may be subject to legal restrictions in your jurisdiction. The authors are not responsible for misuse of this tool.

## Contributing

Feel free to submit issues and enhancement requests!