import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Define the URL of the website
url = 'https://www.sharesansar.com/top-brokers'

# Open the website
driver.get(url)

# Wait until the table with id 'myTable' is found
wait = WebDriverWait(driver, 10)
table = wait.until(EC.presence_of_element_located((By.ID, 'myTable')))

# Parse the HTML content of the table
soup = BeautifulSoup(table.get_attribute('outerHTML'), 'html.parser')

# Initialize an empty list to store the table data
table_data = []

# Find all rows in the table, skipping the header row (if applicable)
rows = soup.find_all('tr')[1:]  # Change index if header row exists

# Iterate over each row and extract data from columns
for row in rows:
    # Find all cells in the row
    cells = row.find_all('td')
    
    # Extract data from each cell and append to the row_data list
    row_data = {
        "S.N.": cells[0].text.strip(),
        "Broker No.": cells[1].text.strip(),
        "Broker Name": cells[2].text.strip(),
        "Buy Amount (Rs.)": cells[3].text.strip(),
        "Sell Amount (Rs.)": cells[4].text.strip(),
        "Total Amount (Rs.)": cells[5].text.strip(),
        "Difference (Rs.)": cells[6].text.strip(),
        "Matching Amount (Rs.)": cells[7].text.strip()
    }
    
    # Append the row data to the table data list
    table_data.append(row_data)

# Close the WebDriver
driver.quit()

# Convert the table data list to JSON format
json_data = json.dumps(table_data, indent=4)

# Print or save the JSON data
print(json_data)

# If you want to save the JSON data to a file, you can do:
with open('jsondata/totalbroker.json', 'w') as json_file:
    json_file.write(json_data)
