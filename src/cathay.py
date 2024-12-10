import os
import time
import requests
from collections import defaultdict
from loguru import logger
from dotenv import load_dotenv


# Configuration
DEPARTURE, ARRIVAL = "HKG", "CTS"
CABIN_CLASSES = {"eco", "pey", "bus"} # or "fir"
PASSENGERS = 2
TARGET_DATES = {"20241228", "20241229"} # YYYYMMDD
DATE_START, DATE_END = "20241227", "20250101" # YYYYMMDD
SLEEP_TIME = 60 # seconds

# Load environment variables
load_dotenv() or logger.error("Failed to load .env file")


def check_availability(departure, arrival, cabin_classes, passengers, date_start=None, date_end=None, target_dates=None):
    cls_map = {"eco": "Economy", "pey": "Premium Economy", "bus": "Business", "fir": "First"}

    date_start = date_start or time.strftime("%Y%m%d")
    date_end = date_end or f"{int(date_start[:4]) + 1}" + date_start[4:]

    base_url = "https://api.cathaypacific.com/afr/search/availability"
    urls = {
        cls: f"{base_url}/zh.{departure}.{arrival}.{cls}.CX.{passengers}.{date_start}.{date_end}.json" 
        for cls in cabin_classes
    }

    try:
        avlb_dates = defaultdict(list)
        for cls, url in urls.items():
            response = requests.get(url).json()
            for date in response.get("availabilities", {}).get("std", []):
                if date["availability"] != "NA" and (not target_dates or date["date"] in target_dates):
                    avlb_dates[date["date"]].append(cls_map[cls])
        return dict(avlb_dates)
    except Exception as e:
        logger.error(f"Error fetching availability: {e}")
        return []

def send_push_notification(title, message):
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

if __name__ == "__main__":
    while True:
        avl_dates = check_availability(
            departure=DEPARTURE,
            arrival=ARRIVAL,
            cabin_classes=CABIN_CLASSES,
            passengers=PASSENGERS,
            date_start=DATE_START,
            date_end=DATE_END,
            target_dates=TARGET_DATES
        )
        if avl_dates:
            logger.success(f"Found: {avl_dates}")
            title = "Asia Miles Redemption"
            message = "Seats available:\n" + "\n".join([f"- {date}: {','.join(cls)}" for date, cls in avl_dates.items()])
            send_push_notification(title, message)
            SLEEP_TIME = 300
        else:
            logger.info(f"Not found, retrying in {SLEEP_TIME} seconds")
        time.sleep(SLEEP_TIME)
