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
import os
import time
import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.APIExtractor import APIExtractor
from utils.DB_Migration import DBMigration
from utils.data_loader import load_test_data
from pages.WebScrapper import WebScrapper, iNetProfitCalculate
import sqlite3
import pandas as pd


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths dynamically based on the project structure
CHROMEDRIVER_PATH = os.path.join(PROJECT_ROOT, "chromedriver.exe")
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, "data", "Data.xlsx")
DATABASE_PATH = os.path.join(PROJECT_ROOT, "data_analysis.db")
REPORT_DIR = os.path.join(PROJECT_ROOT, "tests", "Report")

@pytest.fixture(scope="session")
def config():
    logging.info("Loading test configuration for the session")
    return {
        "base_url": "https://www.screener.in/"
    }


@pytest.fixture
def driver(config):
    logging.info("Initializing WebDriver for test execution")
    service = Service(CHROMEDRIVER_PATH)
    idriver = webdriver.Chrome(service=service)
    idriver.get(config["base_url"])
    logging.info("Navigated to base URL")
    idriver.maximize_window()
    logging.info("Browser window maximized")
    yield idriver
    logging.info("Closing WebDriver after test execution")
    idriver.quit()

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.parametrize("data", load_test_data(DATA_FILE_PATH, "datasheet"))
def test_register(driver, data):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    logger = logging.getLogger()
    logger.info("Starting test for new account registration")
    try:
        # Initialize WebScrapper and perform operations
        logger.info("Initializing WebScrapper for browser interaction")
        wc = WebScrapper(driver)
        logger.info(f"Attempting account registration with email: {data['email']}")
        wc.click_new_account(data["email"], data["passcode"], data["Share"])
        logger.info("Account creation completed successfully")

        logger.info("Starting web scraping process")
        wc.webscrapperextract()
        logger.info("Web scraping completed successfully")

        # Net Profit Calculation
        logger.info("Calculating net profit from extracted data")
        result = iNetProfitCalculate(wc.output_dir)
        logger.info(f"Net profit calculation completed with result: {result}")

        # API Extraction
        logger.info("Initializing API extraction process")
        api = APIExtractor()
        api.apiextract()
        logger.info("API extraction process completed successfully")

        # Database Migration
        logger.info("Starting database migration process")
        output_directory = wc.output_dir
        db_migration = DBMigration(output_dir=output_directory, db_path=DATABASE_PATH)

        # Save data from the latest file to SQLite
        logger.info("Saving data from the latest file into SQLite database")
        db_migration.save_to_sqlite()
        logger.info("Database migration completed successfully")

        # Integration Testing
        logger.info("Performing integration testing on the database")
        db_migration.integration_testing()
        logger.info("Integration testing completed successfully")

    except Exception as e:
        logger.error(f"Error during test execution: {e}")
        raise
