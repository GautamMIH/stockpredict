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
    # Wait until the table with the specified class is found
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'table-bordered'))
    )

    # Parse the HTML content of the table
    soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

    # Find all rows in the table
    rows = soup.find_all('tr')

    # Initialize an empty list to store the table data
    table_data = []

    # Iterate over each row and extract data from columns
    for row in rows[1:]:  # Skip header row if applicable
        # Find all cells in the row
        cells = row.find_all('td')

        # Extract data from each cell and append to the row_data list
        row_data = {
            "Index": cells[0].text.strip(),
            "Open": cells[1].text.strip(),
            "High": cells[2].text.strip(),
            "Low": cells[3].text.strip(),
            "Close": cells[4].text.strip(),
            "Point Change": cells[5].text.strip(),
            "% Change": cells[6].text.strip(),
            "Turnover": cells[7].text.strip()
        }

        # Append the row data to the table data list
        table_data.append(row_data)

    # Convert the table data list to JSON format
    json_data = json.dumps(table_data, indent=4)

    # # Print or save the JSON data
    # print(json_data)

    # If you want to save the JSON data to a file, you can do:
    with open('jsondata/marketindices.json', 'w') as json_file:
        json_file.write(json_data)

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the WebDriver
    driver.quit()
