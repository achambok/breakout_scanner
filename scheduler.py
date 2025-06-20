import schedule
import time
import json
from utils import check_symbol, alert_desktop

def automated_scan():
    with open("watchlist.json", "r") as f:
        symbols = json.load(f)["symbols"]

    results = []
    for sym in symbols:
        result = check_symbol(sym)
        if result:
            results.append(result)

    if results:
        alert_desktop("Breakout Alert 🚨", f"{len(results)} symbols hit breakout.")
        print(f"[{time.ctime()}] {len(results)} symbols hit breakout.")
    else:
        print(f"[{time.ctime()}] No symbols matched.")

# Schedule at 4:01 PM EST
schedule.every().day.at("16:01").do(automated_scan)

print("✅ Scheduled scanner is running...")
while True:
    schedule.run_pending()
    time.sleep(60)
