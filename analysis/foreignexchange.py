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

    # Check if there is a third table
    if len(tables) > 2:
        # Get the third table
        table = tables[2]

        # Parse the HTML content of the third table
        soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

        # Find all rows in the third table
        rows = soup.find_all('tr')

        # Initialize an empty list to store the table data
        table_data = []

        # Iterate over each row and extract data from columns
        for row in rows:
            # Find all cells in the row
            cells = row.find_all('th')

            # Extract data from each cell
            if len(cells) >= 3:  # Ensure that there are at least three cells
                currency = cells[0].text.strip()
                buy = cells[1].text.strip()
                sell = cells[2].text.strip()

                # Append the data to the table_data list as a dictionary
                table_data.append({'currency': currency, 'buy': buy, 'sell': sell})

        # Convert the table data list to JSON format
        json_data = json.dumps(table_data, indent=4)

        # # Print or save the JSON data
        # print(json_data)

        # If you want to save the JSON data to a file, you can do:
        with open('jsondata/foreignexchange.json', 'w') as json_file:
            json_file.write(json_data)

    else:
        print("There are no multiple tables with the specified class.")

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the WebDriver
    driver.quit()
