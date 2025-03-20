import pytest
import os
import csv
from datetime import datetime
from scrape_feeds import DataFeedScraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session")
def credentials():
    """Get test credentials from environment variables or user input."""
    email = os.getenv('SWYM_TEST_EMAIL')
    password = os.getenv('SWYM_TEST_PASSWORD')
    
    if not email or not password:
        print("\nTest credentials not found in environment variables.")
        email = input("\nEnter your email for testing: ")
        password = input("Enter your password for testing: ")
    
    return email, password

@pytest.fixture(scope="session")
def scraper(credentials):
    """Create a scraper instance for testing."""
    email, password = credentials
    scraper = DataFeedScraper(email=email, password=password)
    yield scraper
    scraper.close()

def test_login(scraper):
    """Test the login functionality."""
    try:
        scraper.login()
        # If we get here, login was successful
        assert True
    except Exception as e:
        pytest.fail(f"Login failed with error: {str(e)}")

def test_get_all_feeds(scraper):
    """Test getting all feed data."""
    try:
        # Get feed data
        feeds_data = scraper.get_all_feeds()
        
        # Verify we got data
        assert feeds_data is not None
        assert isinstance(feeds_data, list)
        assert len(feeds_data) > 0
        
        # Verify data structure of first feed
        first_feed = feeds_data[0]
        assert isinstance(first_feed, dict)
        assert len(first_feed) > 0
        
        # Print some info about the data we got
        print(f"\nFound {len(feeds_data)} feeds")
        print(f"Feed data fields: {list(first_feed.keys())}")
    except Exception as e:
        pytest.fail(f"Failed to get feeds: {str(e)}")

def test_save_to_csv(scraper):
    """Test saving feed data to CSV."""
    try:
        # Get feed data
        feeds_data = scraper.get_all_feeds()
        
        # Save to CSV
        csv_file = scraper.save_to_csv(feeds_data)
        
        # Verify file was created
        assert csv_file is not None
        assert os.path.exists(csv_file)
        
        # Verify CSV contents
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == len(feeds_data)
            
            # Print some info about the saved data
            print(f"\nSaved {len(rows)} rows to {csv_file}")
            print(f"CSV headers: {reader.fieldnames}")
        
        # Clean up
        os.remove(csv_file)
        assert not os.path.exists(csv_file)
    except Exception as e:
        pytest.fail(f"Failed to save CSV: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v']) 