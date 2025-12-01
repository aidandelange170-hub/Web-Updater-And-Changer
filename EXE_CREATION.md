# Web Scraper Executable Creation

This project includes a script to convert the web scraper into a standalone executable using PyInstaller.

## Files

- `turn_into_exe.py` - Script to create the executable
- `web_scraper/main_minimal.py` - Minimal version of the scraper optimized for executable creation
- `dist/WebScraperMinimal` - The resulting executable (created after running the script)

## How to Create the Executable

1. Run the executable creation script:
   ```bash
   python turn_into_exe.py
   ```

2. The executable will be created in the `dist/` directory as `WebScraperMinimal`

## Using the Executable

The executable has the following usage:

```bash
./dist/WebScraperMinimal <URL> --output <output_file>
```

Example:
```bash
./dist/WebScraperMinimal https://example.com --output result.json
```

## Notes

- The executable is created from `main_minimal.py` which contains core scraping functionality
- The full-featured version with Google search integration was too complex for PyInstaller to handle efficiently
- The minimal version includes the essential scraping features: title extraction, content extraction, links, and images
- The executable is self-contained and can run without Python or dependencies installed