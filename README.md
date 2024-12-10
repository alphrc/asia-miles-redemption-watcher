# Asia Miles Redemption Availability Watcher

This script helps you secure redemption seats on Cathay Pacific by notifying you in real-time, addressing the significant delays in information update on their website that previously caused me to miss out on the tickets I wanted.

## Requirements
- Python 3.7+
- Pushover account for receiving notifications.
- API credentials stored in a .env file.

## Installation
**1. Clone the repository**
```bash
git clone https://github.com/alphrc/util-asia-miles-redemption-watcher.git
cd util-asia-miles-redemption-watcher
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Install Pushover application on your phone** ([Android](https://pushover.net/clients/android) / [iPhone](https://pushover.net/clients/ios))

**4. Create a `.env` file with the following content:**

The API token and user key can be generated through [Pushover](https://pushover.net/api)

```bash
PUSHOVER_API_TOKEN=your_pushover_api_token
PUSHOVER_USER_KEY=your_pushover_user_key
```

**5. (Optional) Install Chrome 126 and ChromeDriver**
The data from GBA Airline cannot be directly accessed. Chrome and ChromeDriver are needed to scrape the data.

**Chrome**: Install Chrome v126 from [Uptown](https://google-chrome.en.uptodown.com/mac/download/1016453176)

**ChromeDriver**: Find the [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads/canary) of the same version as Chrome for your OS

## Usage

### Cathay Asia Miles Redemption Monitor
**1. Edit the script configuration**
Modify the following variables in the script to suit your preferences:
- `DEPARTURE` and `ARRIVAL`: Departure and arrival airport codes.
- `CABIN_CLASSES`: Cabin classes to monitor ("eco", "pey", "bus", "fir").
- `PASSENGERS`: Number of passengers.
- `TARGET_DATES`: Set of target dates in YYYYMMDD format.
- `DATE_START` and `DATE_END`: Date range to search for availability.
- `SLEEP_TIME`: Retry interval in seconds.

**2. Run the script**
```bash
python src/cathay.py
```

The script will:
1. Check seat availability for the configured routes and dates.
2. Send a push notification when matching seats are found.
3. Retry at the specified interval if no matches are available.

### GBA Airline Price Monitor
```bash
python src/gba.py
```

The script will:
1. Check current price for selected flight, notify you once there's change
2. Check seats availability, notify you once there are limited seats left.
