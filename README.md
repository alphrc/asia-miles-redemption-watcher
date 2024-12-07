# Asia Miles Redemption Availability Watcher

This Python script monitors seat availability for Asia Miles redemption across specified cabin classes, routes, and dates. When seats become available, it sends real-time push notifications using Pushover.

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



## Usage
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
python asia_miles_monitor.py
```
The script will:
1. Check seat availability for the configured routes and dates.
2. Send a push notification when matching seats are found.
3. Retry at the specified interval if no matches are available.