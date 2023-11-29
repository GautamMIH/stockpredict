from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up ChromeOptions
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument('--no-sandbox')  # Added to resolve potential issues in headless mode
chrome_options.add_argument('--disable-dev-shm-usage')  # Added to resolve potential issues in headless mode

# Set up the Chrome webdriver with the provided ChromeDriver in Colab
driver = webdriver.Chrome(options=chrome_options)
url = 'https://www.sharesansar.com/company/nmb#cpricehistory' #change stock link
driver.get(url)

# Find and click the link by ID (replace 'your-link-id' with the actual ID)
link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'btn_cpricehistory')))
link.click()

with open('NMB.csv', 'w', newline='') as csv_file: #change csv name
    csv_writer = csv.writer(csv_file)
    
# Find the table with id 'myTableCPriceHistory' on each iteration
    table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'myTableCPriceHistory')))

    # Extract the header (thead) and write to CSV
    header_row = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    headers = [header.text.strip() for header in header_row]
    csv_writer.writerow(headers)

    while True:
        time.sleep(5)
        # Find the table with id 'myTableCPriceHistory' on each iteration
        table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'myTableCPriceHistory')))

        # Extract the header (thead) and write to CSV
        header_row = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        headers = [header.text.strip() for header in header_row]
        # csv_writer.writerow(headers)

        # Extract the body (tbody) and write each row to CSV
        body_rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
        for row in body_rows:
            data = [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'td')]
            csv_writer.writerow(data)

        # Look for the next page anchor tag and click it if available
        try:
            next_page_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'myTableCPriceHistory_next')))
            if 'disabled' in next_page_link.get_attribute('class').split():
            # No more pages, break the loop
                break
            next_page_link.click()
        except Exception as e:
            # No more pages, break the loop
            break

# Close the browser
driver.quit()