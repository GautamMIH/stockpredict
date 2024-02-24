import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('C:/Users/grim/OneDrive/Desktop/stockpredict/ALICL.csv')

# Extract the year from the "Date" column and create a new "Inflation Rate" column
df['Year'] = pd.to_datetime(df['Date']).dt.year
df['Inflation Rate'] = df['Year'].map({2011: 0.0923, 2012: 0.0946, 2013: 0.0904, 2014: 0.0836, 2015: 0.0787, 2016: 0.0879, 2017:0.0363, 2018:0.0406, 2019:0.0557, 2020:0.0505, 2021: 0.0409, 2022:0.0769, 2023:0.0752, 2024: 0.0752})

# Drop the intermediate "Year" column if you don't need it anymore
df = df.drop(columns=['Year'])

# Save the updated DataFrame to a new CSV file
df.to_csv('SRLI.csv', index=False)
