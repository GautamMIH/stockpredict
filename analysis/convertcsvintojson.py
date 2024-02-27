import pandas as pd
from datetime import datetime, time
import json

# Read CSV file into a pandas DataFrame
selectedstock = 'srli'
df = pd.read_csv(f'stockdata/{selectedstock}.csv')

# Combine Date and Time (14:30) and convert to Unix timestamp
df['Timestamp'] = pd.to_datetime(df['Date'] + ' 14:30')
df['Timestamp'] = df['Timestamp'].astype('int64') // 10**9  # Convert to Unix timestamp

# Remove commas from all columns and convert string values to numeric
for col in df.columns:
    if df[col].dtype == 'object':  # Check if the column contains string values
        df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')

# Drop 'CHANGE' and 'Adjusted_Close' columns
df = df.drop(columns=['CHANGE', 'Adjusted_Close'])

# Convert DataFrame to the desired format
converted_data = df[['Timestamp', 'Open', 'High', 'Low', 'LTP', 'Volume']].values.tolist()

# Reverse the converted data
converted_data.reverse()

# Write JSON data to a file
with open(f'stockdata/{selectedstock}.json', 'w') as f:
    json.dump(converted_data, f)
