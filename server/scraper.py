from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
def scrape_forex_data(from_currency, to_currency, period1, period2):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Set up the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Navigate to the page
    url = f"https://finance.yahoo.com/quote/{from_currency}{to_currency}%3DX/history/?period1={period1}&period2={period2}"
    driver.get(url)

    # Wait for the table to load
    wait = WebDriverWait(driver, 20)
    table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "svelte-ewueuo")))

    # Get the HTML content
    html_content = driver.page_source

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the specific table with class "svelte-ewueuo"
    table = soup.find('table', class_='svelte-ewueuo')

    if table:
        # Extract the headers
        headers = [th.text.strip() for th in table.find('tr').find_all('th')]
        
        # Extract the data
        data = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cols = row.find_all('td')
            if cols:
                data.append([col.text.strip() for col in cols])
        
        # Create a DataFrame
        df = pd.DataFrame(data, columns=headers)
        
        # Close the browser
        driver.quit()
        
        return df
    else:
        driver.quit()
        raise ValueError("Table with class 'svelte-ewueuo' not found in the HTML content.")

# Remove the get_period_start function as it's no longer needed

def get_period_start(period):
    now = int(time.time())
    if period == "1W":
        return now - 7 * 24 * 60 * 60
    elif period == "1M":
        return now - 30 * 24 * 60 * 60
    elif period == "3M":
        return now - 90 * 24 * 60 * 60
    elif period == "6M":
        return now - 180 * 24 * 60 * 60
    elif period == "1Y":
        return now - 365 * 24 * 60 * 60
    else:
        raise ValueError("Invalid period")

if __name__ == "__main__":
    df = scrape_forex_data("GBP", "USD", "1M")
    print(df.head())