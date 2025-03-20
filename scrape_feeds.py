import os
import time
import logging
import csv
from datetime import datetime
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Output to console
        logging.FileHandler('scrape_feeds.log')  # Output to file
    ]
)
logger = logging.getLogger(__name__)

class DataFeedScraper:
    def __init__(self, email=None, password=None):
        self.driver = None
        self.wait = None
        self.email = email
        self.password = password
        logger.info("Initializing DataFeedScraper")
        self.setup_driver()

    def setup_driver(self):
        """Set up the Chrome WebDriver with appropriate options."""
        logger.info("Setting up Chrome WebDriver")
        try:
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless=new')  # Commented out for debugging
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')  # Required for headless mode
            options.add_argument('--window-size=1920,1080')  # Set window size
            options.add_argument('--start-maximized')
            
            # Add logging preferences
            options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
            
            logger.info("Creating Chrome WebDriver with options...")
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_window_size(1920, 1080)
            
            logger.info("Setting up WebDriverWait...")
            self.wait = WebDriverWait(self.driver, 20)
            self.driver.implicitly_wait(20)
            
            logger.info("WebDriver setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup WebDriver: {str(e)}")
            raise

    def login(self):
        """Log in to the SWYM admin interface."""
        try:
            logger.info("Attempting to log in...")
            self.driver.get('https://swym.ai/admin')  # Start with main admin page
            logger.info("Navigated to SWYM admin")
            
            # Wait for login form and enter credentials
            logger.info("Waiting for login form...")
            try:
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, "email"))
                )
                logger.info("Found email field")
                
                password_field = self.driver.find_element(By.ID, "password")
                logger.info("Found password field")
                
                username_field.clear()  # Clear any existing text
                password_field.clear()
                
                username_field.send_keys(self.email)
                password_field.send_keys(self.password)
                logger.info("Entered credentials")
                
                # Find and click login button
                login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
                login_button.click()
                logger.info("Clicked login button")
                
                # Wait for login to complete and redirect
                logger.info("Waiting for login to complete...")
                time.sleep(5)  # Give more time for login processing
                
                # Navigate directly to feeds page
                logger.info("Navigating to feeds page...")
                self.driver.get('https://swym.ai/admin/data/feeds')
                
                # Wait for the table with increased timeout
                logger.info("Waiting for feeds table to load...")
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
                )
                logger.info("Successfully loaded feeds page")
                
            except TimeoutException as te:
                logger.error(f"Timeout while waiting for element: {str(te)}")
                # Log the current page source for debugging
                logger.debug(f"Page source: {self.driver.page_source}")
                raise
                
            except Exception as e:
                logger.error(f"Error during login process: {str(e)}")
                raise
            
        except Exception as e:
            logger.error(f"Failed to login or navigate to feeds page: {str(e)}")
            raise

    def get_all_feeds(self):
        """Get all feed data from the table."""
        try:
            # Wait for table to be present
            table = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
            )
            
            # Get headers
            headers = table.find_elements(By.TAG_NAME, "th")
            header_texts = [header.text.strip() for header in headers]
            
            # Get all rows
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # Skip header row
            
            feeds_data = []
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = {}
                    for i, cell in enumerate(cells):
                        if i < len(header_texts):
                            row_data[header_texts[i]] = cell.text.strip()
                    feeds_data.append(row_data)
                except Exception as e:
                    logger.warning(f"Failed to process row: {str(e)}")
                    continue
            
            return feeds_data
            
        except Exception as e:
            logger.error(f"Error getting feed data: {str(e)}")
            return []

    def save_to_csv(self, feeds_data):
        """Save feed data to CSV file."""
        if not feeds_data:
            logger.warning("No feed data to save")
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"feed_data_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = feeds_data[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for feed in feeds_data:
                    writer.writerow(feed)
                    
            logger.info(f"Successfully saved feed data to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {str(e)}")
            return None

    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed")

def main():
    """Main function to run the scraper."""
    print("\nSWYM Data Feed Scraper")
    print("=====================")
    
    # Get credentials securely
    email = input("\nEnter your email: ")
    password = getpass.getpass("Enter your password: ")
    
    scraper = None
    try:
        scraper = DataFeedScraper(email=email, password=password)
        scraper.login()
        feeds_data = scraper.get_all_feeds()
        
        if feeds_data:
            csv_file = scraper.save_to_csv(feeds_data)
            if csv_file:
                print(f"\nFeed data saved to: {csv_file}")
                print(f"Total feeds processed: {len(feeds_data)}")
            else:
                print("Failed to save feed data")
        else:
            print("No feed data found")
            
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main() 