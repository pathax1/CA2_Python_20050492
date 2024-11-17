# ***************************************************************************************************************************************************************************************
# Framework Type: Data Driven Framework
# Description: This framework automates the process of registering a new account, searching for a company, and extracting quarterly financial data
#              from a webpage. It uses Selenium WebDriver for browser interaction and a data-driven approach to load test data dynamically from an Excel file.
# Parameters:
#   - driver: Selenium WebDriver instance for browser automation.
#   - data: Dictionary containing test data loaded from the Excel file, including email, password, and company/share details.
# Website : https://www.screener.in/home/
# Author: Aniket Pathare | 20050492@mydbs.ie
# Precondition:
#   - The Chrome WebDriver executable must be installed and its path specified in the script.
#   - The Excel file with required test data (email, passcode, and share) should be populated and located at the specified path.
#   - The webpage (https://www.screener.in/) should be accessible.
# Date Created: 2024-11-17
# ****************************************************************************************************************************************************************************************
import time
import pytest
from selenium import webdriver
from utils.data_loader import load_test_data
from pages.HomePage import HomePage
from selenium.webdriver.chrome.service import Service
import requests

@pytest.fixture(scope="session")
def config():
    return {
        "base_url": "https://www.screener.in/"
    }

@pytest.fixture
def driver(config):
    service = Service("C:/Users/anike/PycharmProjects/Automation_API_Extract/chromedriver.exe")
    idriver = webdriver.Chrome(service=service)
    idriver.get(config["base_url"])
    idriver.maximize_window()
    yield idriver
   # idriver.quit()

@pytest.mark.parametrize("data", load_test_data(r"C:\Users\anike\PycharmProjects\Automation_API_Extract\data\Data.xlsx", "datasheet"))
def test_register(driver, data):
    hp = HomePage(driver)
    hp.click_new_account(data["email"], data["passcode"],data["Share"])  # Pass the arguments here
    #hp.extractWebTable()
    hp.extract_api()