import json
from selenium import webdriver
from bs4 import BeautifulSoup

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Open the website
driver.get("https://www.nepsealpha.com/api/get_map_data?fs=25-5-37")

# Extract the response content
response_content = driver.page_source

# Close the WebDriver
driver.quit()

# Clean HTML tags using BeautifulSoup
soup = BeautifulSoup(response_content, "html.parser")
cleaned_content = soup.get_text()

# Encode the cleaned content as JSON
encoded_json = json.dumps({"response_content": cleaned_content}, ensure_ascii=False)
# Remove backslashes before double quotes
encoded_json = encoded_json.replace('\\\"', '\"')
# Remove double quotes before the second '{'
encoded_json = encoded_json.replace('"{"', '{"', 1)

# Remove double quotes before the last '}'
encoded_json = encoded_json[::-1].replace('}"', '}', 1)[::-1]

# Save the JSON data to a file
with open("heatmap.json", "w") as json_file:
    json_file.write(encoded_json)

print("JSON data saved to heatmap.json file.")
