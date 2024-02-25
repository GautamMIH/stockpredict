import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define the URL of the website
url = 'https://www.sharesansar.com/market'

# Open the website
driver.get(url)

try:
    # Wait until all tables with the specified class are found
    tables = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'table-bordered'))
    )

    # Check if there is at least a second table
    if len(tables) > 1:
        # Get the second table
        table = tables[1]

        # Parse the HTML content of the second table
        soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

        # Find all rows in the second table
        rows = soup.find_all('tr')

        # Initialize an empty list to store the table data
        table_data = []

        # Iterate over each row and extract data from columns
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('td')

            # Extract data from each cell and append to the row_data list
            row_data = [cell.text.strip() for cell in cells]

            # Append the row data to the table data list
            table_data.append(row_data)

        # Convert the table data list to JSON format
        json_data = json.dumps(table_data, indent=4)

        # # Print or save the JSON data
        # print(json_data)

        # If you want to save the JSON data to a file, you can do:
        with open('jsondata/marketsummary.json', 'w') as json_file:
            json_file.write(json_data)

    else:
        print("There are no multiple tables with the specified class.")

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the WebDriver
    driver.quit()
