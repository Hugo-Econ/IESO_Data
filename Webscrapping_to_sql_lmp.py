# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 14:54:50 2025

@author: Hugo
"""

import os
from io import StringIO
import re
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# === CONFIGURATION ===
BASE_URL = "https://reports-public.ieso.ca/public/RealtimeEnergyLMP/"
MONTH_PREFIX = "202507"  # July 2025

# Windows-safe path
BASE_SAVE_DIR = r"C:\Users\Hugo\Dropbox\1. School\1.Research\Ontario_Storage\Data_IESO"
#CSV_SAVE_DIR = os.path.join(BASE_SAVE_DIR, "ieso_july_lmp")
DB_PATH = os.path.join(BASE_SAVE_DIR, "realtime_lmp_2025_07.sqlite")
TABLE_NAME = "lmp_data"

#os.makedirs(CSV_SAVE_DIR, exist_ok=True)

# === STEP 1: Scrape the report page ===
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, "html.parser")

# === STEP 2: Filter links for July 2025 ===
all_links = [
    link['href'] for link in soup.find_all('a', href=True)
    if link['href'].startswith(f"PUB_RealtimeEnergyLMP_{MONTH_PREFIX}")
    and link['href'].endswith('.csv')
]

# === STEP 3: Keep only the latest version of each file ===
latest_files = {}
pattern = re.compile(r'PUB_RealtimeEnergyLMP_(\d{10})_v(\d+)\.csv')

for link in all_links:
    match = pattern.match(link)
    if match:
        hour_key = match.group(1)
        version = int(match.group(2))
        if hour_key not in latest_files or version > latest_files[hour_key][1]:
            latest_files[hour_key] = (link, version)

# === STEP 4: Open SQLite DB ===
conn = sqlite3.connect(DB_PATH)

# Clear broken table schema
conn.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
conn.commit()



# === STEP 5: Download, Read, and Insert CSVs (No disk writes) ===
for hour_key, (filename, version) in latest_files.items():
    file_url = urljoin(BASE_URL, filename)

    # Extract date info from filename
    match = re.search(r'PUB_RealtimeEnergyLMP_(\d{4})(\d{2})(\d{2})(\d{2})', filename)
    if match:
        year, month, day, hour = match.groups()
        date_str = f"{year}-{month}-{day}"
        datetime_str = f"{year}-{month}-{day} {hour}:00:00"
    else:
        print(f"⚠️ Could not parse date from filename: {filename}")
        continue

    # Download and load from memory
    try:
        print(f"📥 Downloading and processing: {filename}")
        r = requests.get(file_url)
        r.raise_for_status()

        # Read CSV from response text
        df = pd.read_csv(StringIO(r.text), skiprows=1, index_col=False)

        # Add metadata columns
        df['source_file'] = filename
        df['Year'] = int(year)
        df['Month'] = int(month)
        df['Day'] = int(day)
        df['Date'] = pd.to_datetime(date_str)
        df['Datetime'] = pd.to_datetime(datetime_str)

        # Reorder columns
        desired_order = [
            'Year', 'Month', 'Day', 'Date', 'Datetime',
            'Delivery Hour', 'Interval', 'Pricing Location', 'LMP',
            'Energy Loss Price', 'Energy Congestion Price', 'source_file'
        ]
        df = df[desired_order]

        # Insert into SQLite
        df.to_sql(TABLE_NAME, conn, if_exists='append', index=False)
        print(f"✅ Imported: {filename}")
    except Exception as e:
        print(f"⚠️ Error processing {filename}: {e}")

conn.close()

df.columns


DB_PATH = r"C:\Users\Hugo\Dropbox\1. School\1.Research\Ontario_Storage\Data_IESO\realtime_lmp_2025_07.sqlite"
conn = sqlite3.connect(DB_PATH)

query = """
SELECT *
FROM lmp_data
WHERE Year = 2025 AND Month = 7 AND Day = 10
"""
df_test = pd.read_sql(query, conn)
df_test

conn.close()