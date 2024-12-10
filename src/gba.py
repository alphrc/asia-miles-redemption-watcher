import os
import requests
import time
from loguru import logger
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
if not load_dotenv():
    logger.error("Failed to load .env file")

# Configure Chrome options for headless mode
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--log-level=3")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Automatically manage ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
logger.info("ChromeDriver initialized successfully")


def send_push_notification(title: str, message: str):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": os.getenv("PUSHOVER_API_TOKEN"),
        "user": os.getenv("PUSHOVER_USER_KEY"),
        "title": title,
        "message": message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        logger.success("Notification sent successfully!")
    except Exception as e:
        logger.error(f"Error sending notification: {e}")

def monitor_flight_price():
    url = "https://trp.greaterbay-airlines.com/cn-HK/flights/results/HKG-CTS-241229-900-0"
    latest_price = None

    while True:
        driver.get(url)
        time.sleep(10)

        try:
            price_element = driver.find_element(By.CSS_SELECTOR, "div.fsifv-cabin-card div.cabin-price span.money-num")
            current_price = int(price_element.text.replace(",", ""))
            logger.info(f"Current price: ${current_price}")
            if latest_price is not None and current_price != latest_price:
                send_push_notification("GBA Flight Price Alert", f"Price changed from ${latest_price} to ${current_price}")
            latest_price = current_price
        except Exception as e:
            logger.error(f"Failed to extract price: {e}")

        try:
            status_element = driver.find_element(By.CSS_SELECTOR, "div.fsifv-cabin-card div.ticket-num")
            seat_status = status_element.text
            logger.info(f"Seat status: {seat_status or 'Available'}")

            if seat_status == "尚餘少量機位":
                send_push_notification("Seat Availability Warning", "Limited seats available!")
        except Exception:
            logger.warning("Seat availability information not found")

        logger.info("Waiting for 1 minute before the next check...")
        time.sleep(60)

def cleanup():
    logger.info("Closing ChromeDriver...")
    driver.quit()
    logger.info("ChromeDriver closed successfully")

if __name__ == "__main__":
    try:
        monitor_flight_price()
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
    finally:
        cleanup()