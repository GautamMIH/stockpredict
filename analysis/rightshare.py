import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Chrome WebDriver
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Define the URL of the website
url = 'https://www.sharesansar.com/existing-issues'

# Open the website
driver.get(url)
# link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, '#rightshare')))
# link.click()
right_share_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[text()="Right Share"]'))
    )

    # Click on the "Right Share" tab
right_share_tab.click()

try:
    # Initialize an empty list to store the table data
    table_data = []

    # Scrape data from all pages
    while True:
        time.sleep(1)
        # Wait until the table is found
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'myTableErs'))
        )

        # Parse the HTML content of the table
        soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

        # Find all rows in the table
        rows = soup.find_all('tr')

        # Iterate over each row and extract data from columns
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('td')

            # Extract data from each cell
            if len(cells) >= 8:  # Ensure that there are at least three cells
                sn = cells[0].text.strip()
                symbol = cells[1].text.strip()
                Company = cells[2].text.strip()
                Ratio = cells[3].text.strip()
                Units = cells[4].text.strip()
                Price= cells[5].text.strip()
                OpeningDate = cells[6].text.strip()
                ClosingDate = cells[7].text.strip()
                LClosingDate = cells[8].text.strip()
                ListingDate = cells[9].text.strip()
                IssueManager = cells[10].text.strip()
                Status = cells[11].text.strip()

                # Append the data to the table_data list as a dictionary
                table_data.append({'SN': sn, 'Symbol': symbol, 'Company': Company, 'Units': Units, 'Price':Price, 'Opening Date':OpeningDate, 'Closing Date':ClosingDate, 'Last Closing Date':LClosingDate, 'Listing Date':ListingDate, 'Issue Manager':IssueManager, 'Status':Status})

        # Check if the next button is disabled
        try:
            next_page_link = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, 'myTableErs_next')))
            if 'disabled' in next_page_link.get_attribute('class').split():
            # No more pages, break the loop
                break
            next_page_link.click()
        except Exception as e:
            # No more pages, break the loop
            break
except Exception as e:
    print("Error occurred:", e)

finally:
    # Convert the table data list to JSON format
    json_data = json.dumps(table_data, indent=4)

    # Save the JSON data to a file
    with open('jsondata/rightshare.json', 'w') as json_file:
        json_file.write(json_data)

    # Close the WebDriver
    driver.quit()
