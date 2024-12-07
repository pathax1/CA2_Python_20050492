import os
import pandas as pd
from datetime import datetime
import requests
from openpyxl import load_workbook

class APIExtractor:
    def __init__(self):
        # Initialize API URL and headers
        self.api_url = "https://www.screener.in/api/company/3370/chart/?q=Price-DMA50-DMA200-Volume&days=30&consolidated=true"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-IE,en-US;q=0.9,en-GB;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://www.screener.in/company/TATAMOTORS/consolidated/",
            "X-Requested-With": "XMLHttpRequest",
            "Cookie": "theme=dark; csrftoken=T34gulGh3neE032waB4HaDRaWuXnDWdW; sessionid=p2atl83lxwtectakpyivr4l9n21p814h"
        }
        self.output_dir = "C:\\Users\\anike\\PycharmProjects\\Automation_API_Extract\\Report"

    # ***************************************************************************************************************************************************************************************
    # Function Name: clean_data
    # Description: This function processes and organizes raw data retrieved from an API into a structured tabular format with two columns: 'Date' and 'Value'.
    # Steps:
    #   1. Iterate through the 'datasets' in the raw data.
    #   2. Extract 'values' from each dataset and validate their structure.
    #   3. Append valid 'Date' and 'Value' pairs to a list.
    #   4. Convert the cleaned list into a Pandas DataFrame.
    #   5. Format the 'Date' column as a datetime object for consistency.
    # Parameters:
    #   - raw_data: A dictionary containing the raw API data to be cleaned and structured.
    # Returns:
    #   - df_cleaned: A Pandas DataFrame containing the cleaned data with 'Date' and 'Value' columns.
    # Author: Aniket Pathare | 20050492@mydbs.ie
    # Precondition: Input data must include a 'datasets' key with nested 'values' lists, each containing exactly two elements (Date and Value).
    # Date Created: 2024-11-17
    # ***************************************************************************************************************************************************************************************

    def clean_data(self, raw_data):
        """
        Cleans and organizes the raw API data into a tabular format with only Date and Value columns.
        """
        cleaned_data = []
        for entry in raw_data.get('datasets', []):
            for value in entry.get('values', []):
                if len(value) == 2:
                    cleaned_data.append({
                        "Date": value[0],
                        "Value": value[1]
                    })
        df_cleaned = pd.DataFrame(cleaned_data)
        # Convert Date column to datetime
        df_cleaned['Date'] = pd.to_datetime(df_cleaned['Date'])
        return df_cleaned

    # ***************************************************************************************************************************************************************************************
    # Function Name: apiextract
    # Description: This function fetches data from a given API, cleans and organizes the data, and appends it to the most recent Excel file in a specified directory.
    # Steps:
    #   1. Send a GET request to the API.
    #   2. Parse the JSON response and validate the status code.
    #   3. Clean and structure the data to retain relevant columns.
    #   4. Identify the latest Excel file in the output directory based on the timestamp.
    #   5. Append the cleaned data as a new sheet in the existing Excel file.
    # Parameters: None
    # Author: Aniket Pathare | 20050492@mydbs.ie
    # Precondition: The output directory should contain at least one Excel file, and the API should be accessible with valid credentials.
    # Date Created: 2024-11-17
    # ***************************************************************************************************************************************************************************************

    def apiextract(self):
        try:
            # Step 1: Send the GET request
            response = requests.get(self.api_url, headers=self.headers)

            # Step 2: Check response status
            if response.status_code == 200:
                print("API request successful!")

                # Step 3: Parse the JSON response
                raw_data = response.json()

                # Step 4: Clean and organize the data
                cleaned_data = self.clean_data(raw_data)

                # Step 5: Identify the most recent Excel file
                excel_files = [f for f in os.listdir(self.output_dir) if f.endswith('.xlsx')]
                if not excel_files:
                    raise FileNotFoundError("No Excel file found in the directory.")

                # Get the latest file based on timestamp
                latest_file = max(
                    (os.path.join(self.output_dir, f) for f in excel_files),
                    key=os.path.getmtime
                )

                # Step 6: Save cleaned data to a new sheet in the existing Excel file
                with pd.ExcelWriter(latest_file, mode='a', engine='openpyxl') as writer:
                    cleaned_data.to_excel(writer, index=False, sheet_name="Cleaned API Data")
                print(f"Cleaned API data added to {latest_file} in a new sheet 'Cleaned API Data'.")
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")
                print(f"Error response: {response.text}")
        except Exception as e:
            print(f"An error occurred: {e}")
