# SWYM Data Feeds Scraper

A Python script to scrape feed data from the SWYM admin interface and save it to CSV. This tool automates the process of collecting feed information from the SWYM admin dashboard and exports it to a structured CSV format.

## Features

- Automated login to SWYM admin interface
- Scrapes all feed data from the feeds table
- Saves data to timestamped CSV files
- Comprehensive logging
- Unit tests for core functionality
- Error handling and retry mechanisms
- Configurable wait times for page loading

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by webdriver-manager)
- Git (for cloning the repository)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd swym_datafeeds
```

2. Create and activate a virtual environment (recommended):
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your credentials:
```
FEED_URL=https://swym.ai/admin
FEED_USERNAME=your_username
FEED_PASSWORD=your_password
```

## Dependencies

The project requires the following Python packages:
- `selenium==4.18.1`: For web automation
- `python-dotenv==1.0.1`: For environment variable management
- `webdriver-manager==4.0.1`: For ChromeDriver management

## Usage

### Basic Usage

Run the scraper with default settings:
```bash
python scrape_feeds.py
```

### Output

The script will:
1. Log in to the SWYM admin interface
2. Navigate to the feeds page
3. Scrape all feed data
4. Save the data to a CSV file with timestamp
5. Display the results in the console

The output CSV file will be named `feed_data_YYYYMMDD_HHMMSS.csv` and will contain all feed data with headers matching the table columns.

## Code Structure

### Main Components

1. `DataFeedScraper` class:
   - Handles browser automation
   - Manages login and navigation
   - Scrapes feed data
   - Exports data to CSV

2. Key Methods:
   - `setup_driver()`: Configures Chrome WebDriver
   - `login()`: Handles authentication
   - `get_all_feeds()`: Scrapes feed data
   - `save_to_csv()`: Exports data to CSV
   - `close()`: Cleans up resources

### Logging

The script provides comprehensive logging:
- Console output for real-time monitoring
- Log file (`scrape_feeds.log`) for debugging
- Log levels: INFO, WARNING, ERROR

## Testing

### Running Tests

Run the unit tests:
```bash
python -m unittest test_scrape_feeds.py
```

### Test Coverage

The test suite covers:
- Login functionality
- Feed data extraction
- CSV file generation
- Error handling
- Browser setup and cleanup

## Error Handling

The script includes robust error handling for:
- Network issues
- Login failures
- Stale elements
- File system errors
- Browser automation issues

## Troubleshooting

Common issues and solutions:

1. ChromeDriver issues:
   - Ensure Chrome browser is up to date
   - Check webdriver-manager is properly installed

2. Login failures:
   - Verify credentials in `.env` file
   - Check network connectivity
   - Ensure FEED_URL is correct

3. Stale element errors:
   - Increase wait times in the script
   - Check for slow network conditions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Add your license information here]

## Support

For support, please:
1. Check the troubleshooting section
2. Review the logs in `scrape_feeds.log`
3. Create an issue in the repository 