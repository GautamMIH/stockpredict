from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time

# Set up ChromeOptions
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument('--no-sandbox')  # Added to resolve potential issues in headless mode
chrome_options.add_argument('--disable-dev-shm-usage')  # Added to resolve potential issues in headless mode

# Set up the Chrome webdriver with the provided ChromeDriver in Colab
driver = webdriver.Chrome(options=chrome_options)
psymbol = 'licn'
url = f'https://www.sharesansar.com/company/{psymbol}'
driver.get(url)

# Find and click the link by ID (replace 'your-link-id' with the actual ID)
link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'btn_cpricehistory')))
link.click()

# Connect to SQLite database (create a new database file if it doesn't exist)
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS NLIC (
#         SN TEXT,
#         Date TEXT,
#         Open TEXT,
#         High TEXT,
#         Low TEXT,
#         LTP TEXT,
#         CHANGE TEXT,
#         Volume TEXT,
#         Adjusted_Close TEXT
#     )
# ''')
query = f'''
    CREATE TABLE IF NOT EXISTS {psymbol} (
        SN TEXT,
        Date TEXT,
        Open TEXT,
        High TEXT,
        Low TEXT,
        LTP TEXT,
        CHANGE TEXT,
        Volume TEXT,
        Adjusted_Close TEXT
    )
'''
cursor.execute(query)

while True:
    time.sleep(3)
    # Find the table with id 'myTableCPriceHistory' on each iteration
    table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'myTableCPriceHistory')))

    # Extract the body (tbody) and write each row to the database
    body_rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
    for row in body_rows:
        data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')]
        query = f'''
          INSERT INTO {psymbol} (SN, Date, Open, High, Low, LTP, CHANGE, Volume, Adjusted_Close)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
        cursor.execute(query, data)

    # Commit the changes to the database
    conn.commit()

    # Look for the next page anchor tag and click it if available
    try:
        next_page_link = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'myTableCPriceHistory_next')))
        if 'disabled' in next_page_link.get_attribute('class').split():
            # No more pages, break the loop
                break
        next_page_link.click()
    except Exception as e:
        # No more pages, break the loop
        break

# Close the database connection
conn.close()

# Close the browser
driver.quit()
