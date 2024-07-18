import schedule
import time
from scraper import scrape_forex_data
from database import get_db

def update_forex_data():
    currency_pairs = [("GBP", "INR"), ("AED", "INR")]
    periods = ["1W", "1M", "3M", "6M", "1Y"]

    for from_currency, to_currency in currency_pairs:
        for period in periods:
            try:
                df = scrape_forex_data(from_currency, to_currency, period)
                df.to_sql(f"{from_currency}_{to_currency}_{period}", get_db(), if_exists='replace', index=False)
                print(f"Updated {from_currency}-{to_currency} for period {period}")
            except Exception as e:
                print(f"Error updating {from_currency}-{to_currency} for period {period}: {str(e)}")

def run_scheduler():
    schedule.every().day.at("00:00").do(update_forex_data)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()