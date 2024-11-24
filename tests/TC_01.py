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

from pages.APIExtractor import APIExtractor
from utils.data_loader import load_test_data
from pages.WebScrapper import WebScrapper, iNetProfitCalculate
from selenium.webdriver.chrome.service import Service
import requests
import logging

@pytest.fixture(scope="session")
def config():
    logging.info("Loading test configuration for the session")
    return {
        "base_url": "https://www.screener.in/"
    }

@pytest.fixture
def driver(config):
    logging.info("Initializing WebDriver for test execution")
    service = Service("C:/Users/anike/PycharmProjects/Automation_API_Extract/chromedriver.exe")
    idriver = webdriver.Chrome(service=service)
    idriver.get(config["base_url"])
    logging.info("Navigated to base URL")
    idriver.maximize_window()
    logging.info("Browser window maximized")
    yield idriver
    logging.info("Closing WebDriver after test execution")
    # idriver.quit()

@pytest.mark.parametrize("data", load_test_data(r"C:\Users\anike\PycharmProjects\Automation_API_Extract\data\Data.xlsx", "datasheet"))
def test_register(driver, data):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger()
    logger.info("Starting test for new account registration")
    try:
        logger.info("Initializing WebScrapper for browser interaction")
        wc = WebScrapper(driver)
        logger.info(f"Attempting account registration with email: {data['email']}")
        wc.click_new_account(data["email"], data["passcode"], data["Share"])
        logger.info("Account creation completed successfully")

        logger.info("Starting web scraping process")
        wc.webscrapperextract()
        logger.info("Web scraping completed successfully")

        logger.info("Calculating net profit from extracted data")
        result = iNetProfitCalculate(wc.output_dir)
        logger.info(f"Net profit calculation completed with result: {result}")

        logger.info("Initializing API extraction process")
        api = APIExtractor()
        api.apiextract()
        logger.info("API extraction process completed successfully")

    except Exception as e:
        logger.error(f"Error during test execution: {e}")
        raise
