#Import Essential Libraries to perform execution
import os
import time
from struct import pack_into
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from utils.CommonFunctions import iaction
from selenium.webdriver.common.keys import Keys
import logging



# ***************************************************************************************************************************************************************************************
# Constructor Name: __init__
# Description: The constructor is used to store all the Web Element Properties
# Parameters: driver
# Author:Aniket Pathare | 20050492@mydbs.ie
# Precondition: User should populate the desired values to enter the datasheet prior to the execution
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************
class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.iNewAccount = "//a[@class='button account button-secondary']"
        self.driver = driver
        self.email_input =  "//input[@id='id_email']"
        self.email_input2 = "//input[@id='id_email2']"
        self.password_input = "//input[@id='id_password']"
        self.submit = "//button[normalize-space()='Create account']"
        self.iseachbar="//div[@id='desktop-search']//input[@placeholder='Search for a company']"
        self.imenuitem="//a[normalize-space()='Quarters']"
        self.iWebtable="//section[@id='quarters']//table[@class='data-table responsive-text-nowrap']"

# ***************************************************************************************************************************************************************************************
# Function Name: click_new_account
# Description: This function performs the actions to create a new account, search for a company, and navigate to the 'Quarters' menu item.
# Parameters:
#   - email: The email address for account creation.
#   - password: The password for the new account.
#   - share: The company name or keyword to search in the search bar.
# Author: Aniket Pathare | 20050492@mydbs.ie
# Precondition: User should populate the desired values to enter the datasheet prior to the execution
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************
    def click_new_account(self,email,password,share):
        # Click the 'Create New Account' button
        iaction(self.driver, "Button", "XPATH", self.iNewAccount)
        time.sleep(5)

        # Enter the email address in the email input field
        iaction(self.driver, "Textbox", "XPATH", self.email_input, email)

        # Enter the same email in the email confirmation field
        iaction(self.driver, "Textbox", "XPATH", self.email_input2, email)

        # Enter the password in the password input field
        iaction(self.driver, "Textbox", "XPATH", self.password_input, password)

        # Click the 'Submit' button to create the account
        iaction(self.driver, "Button", "XPATH", self.submit)
        time.sleep(5)

        # Enter the company/share keyword in the search bar
        iaction(self.driver, "Textbox", "XPATH", self.iseachbar,share)
        time.sleep(5)

        # Locate the search bar element and simulate pressing 'Enter'
        search_bar = self.driver.find_element("xpath", self.iseachbar)
        search_bar.send_keys(Keys.RETURN)

        # Navigate to the 'Quarters' link section
        iaction(self.driver, "Hyperlink", "XPATH", self.imenuitem)
        time.sleep(5)

# ***************************************************************************************************************************************************************************************
# Function Name: extract_api
# Description: This function extracts quarterly financial data from a dynamically loaded webpage using Selenium and BeautifulSoup.
#              It parses the HTML to locate the required table, processes the data into a Pandas DataFrame, and saves it to an Excel file.
# Parameters:
#   - self: The instance of the class calling this function, containing the Selenium driver object.
# Author: Aniket Pathare | 20050492@mydbs.ie
# Precondition:
#   - Quaterly Report of the share price page should contain values of the share price.
#   - A valid Selenium WebDriver instance (`self.driver`) must be initialized and logged into the webpage containing the target table.
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************

    def extract_api(self):
        try:
            # Step 1: Get the current URL from the Selenium driver
            url = self.driver.current_url

            # Step 2: Send a GET request to fetch the page content
            response = requests.get(url)

            # Raise an HTTPError for bad responses (4xx and 5xx)
            response.raise_for_status()

            # Step 3: Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Step 4: Locate the section with id "quarters"
            section = soup.find('section', {'id': 'quarters'})
            if not section:
                raise ValueError("Section with id 'quarters' not found.")

            # Step 5: Locate the table within the section
            table = section.find('table')
            if not table:
                raise ValueError("Table in the 'quarters' section not found.")

            # Step 6: Extract table headers
            headers = [header.text.strip() for header in table.find_all('th')]

            # Step 7: Extract table rows
            rows = []
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    rows.append([col.text.strip() for col in columns])

            # Step 8: Create a Pandas DataFrame from the extracted data
            df = pd.DataFrame(rows, columns=headers)

            # Step 9: Clean the DataFrame by dropping the last row (e.g., "Raw PDF")
            df_cleaned = df[:-1]

            # Print the cleaned DataFrame (for debugging or validation)
            print(df_cleaned)

            # Step 10: Define the output directory and ensure it exists
            output_dir = "C:\\Users\\anike\\PycharmProjects\\Automation_API_Extract\\Report"
            os.makedirs(output_dir, exist_ok=True)

            # Step 11: Generate a timestamped file name for the output Excel file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = os.path.join(output_dir, f"extracted_data_{timestamp}.xlsx")

            # Step 12: Save the cleaned DataFrame to an Excel file
            df_cleaned.to_excel(file_name, index=False)
            print(f"Data successfully extracted and saved to {file_name}.")

        except Exception as e:
            # Handle exceptions and display error messages
            print(f"An error occurred: {e}")

