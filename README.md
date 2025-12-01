# Web Scraper and Extractor

A comprehensive web scraping tool built with Python that can extract content from websites.

## Features

- Web scraping with both requests-based and Selenium support
- Google search integration to find relevant URLs
- Content extraction (titles, text, links, images)
- Multiple output formats (JSON and CSV)
- Configurable settings and error handling
- Command-line interface and Python API
- Executable creation with PyInstaller

## Executable Version

This project also includes a script to create a standalone executable of the web scraper:

- Run `python turn_into_exe.py` to create the executable
- The executable will be available as `./dist/WebScraperMinimal`
- It's a self-contained program that can run without Python installed
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

bash
pip install -r requirements.txt


## Usage

### Basic Usage

bash
python main.py "search query" [number_of_results]


Example:
bash
python main.py "python web scraping" 5


### Advanced Usage

You can also run individual components:

# Scrape a specific UR
python -c "from main import WebScraper; s = WebScraper(); result = s.scrape_page('https://example.com'); print(result['title'])"

## Configuration

The scraper can be configured using the `config/config.json` file:

- scraper_settings: Configure scraping behavior
- output_settings: Configure output format and locations
- google_settings: Configure Google search parameters

## Project Structure


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


## Output

The scraper generates:

- JSON files with detailed scraping results
- CSV files with summary information
- Log files for debugging

## Legal Notice

Please use this tool responsibly and respect websites' `robots.txt` files and terms of service. Web scraping may be subject to legal restrictions in your jurisdiction. The authors are not responsible for misuse of this tool.

## Contributing

Feel free to submit issues and enhancement requests!
