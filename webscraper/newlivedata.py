import sqlite3
import csv
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# Specify the path for the CSV file with symbols
url_file_path = '/content/drive/MyDrive/content/COMPANYSYMBOLS.csv'
database_path = '/content/drive/MyDrive/content/company_data.db'

# Read symbols from the CSV file
with open(url_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Assuming the symbols are in the first column (change the index if needed)
    symbols = [row[0] for row in csv_reader]

# Connect to SQLite database
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

# # Create a table if it doesn't exist
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS company_data (
#         Symbol TEXT PRIMARY KEY,
#         AsOn TEXT,
#         CompanyPrice TEXT,
#         CompanyRatio TEXT,
#         CompanyPercent TEXT,
#         Open TEXT,
#         High TEXT,
#         Low TEXT,
#         Volume TEXT
#     )
# ''')

# Loop through each symbol
for symbol in symbols:
    cleaned_symbol = symbol.strip()

    # Construct the URL
    url = f'https://www.sharesansar.com/company/{cleaned_symbol}'
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        div_element = soup.find('div', class_='col-md-7 col-sm-7 col-xs-12')
        comp_ason_span = div_element.find('span', class_='comp-ason')

          # Find the inner span with class "text-org" inside comp-ason span
        inner_span = comp_ason_span.find('span', class_='text-org')

            # Extract the text content of the inner span
        as_on = inner_span.text.strip()
        comp_price = div_element.find('span', class_='comp-price').text
        comp_ratio = div_element.find('span', class_='comp-ratio').text
        comp_percent = div_element.find('span', class_='comp-percent').text

        div_element = soup.find('div', class_='second-row margin-bottom-15')
        spans = div_element.find_all('span')
        open_span = spans[0].find('span', class_='text-org')
        open_value = open_span.next_sibling.strip() if open_span else ''

        high_span = spans[2].find('span', class_='text-org')
        high_value = high_span.next_sibling.strip() if high_span else ''

        low_span = spans[4].find('span', class_='text-org')
        low_value = low_span.next_sibling.strip() if low_span else ''

        volume_span = spans[6].find('span', class_='text-org')
        volume_value = volume_span.next_sibling.strip() if volume_span else ''

        # Check if the record already exists
        cursor.execute('SELECT * FROM company_data WHERE Symbol = ?', (cleaned_symbol,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Update the existing record
            cursor.execute('''
                UPDATE company_data
                SET AsOn=?, CompanyPrice=?, CompanyRatio=?, CompanyPercent=?, Open=?, High=?, Low=?, Volume=?
                WHERE Symbol=?
            ''', (as_on, comp_price, comp_ratio, comp_percent, open_value, high_value, low_value, volume_value, cleaned_symbol))
        else:
            # Insert a new record
            cursor.execute('''
                INSERT INTO company_data (Symbol, AsOn, CompanyPrice, CompanyRatio, CompanyPercent, Open, High, Low, Volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cleaned_symbol, as_on, comp_price, comp_ratio, comp_percent, open_value, high_value, low_value, volume_value))

# Commit changes and close the connection
connection.commit()
connection.close()
