import sqlite3
import pandas as pd
import os


class DBMigration:


    def __init__(self, output_dir, db_path="data_analysis.db"):
        # Directory where Excel files are stored
        self.output_dir = output_dir
        # Path to the SQLite database file
        self.db_path = db_path

    # ***************************************************************************************************************************************************************************************
    # Function Name: save_to_sqlite
    # Description: This function processes the latest Excel file from a specified output directory, extracts data from all its sheets, and saves the data to an SQLite database.
    # Steps:
    #   1. Establish a connection to the SQLite database (creates a new file if it doesn't exist).
    #   2. Fetch all Excel files in the output directory.
    #   3. Identify the most recently modified Excel file.
    #   4. Read the file and iterate through all its sheets.
    #   5. Standardize column names for SQLite compatibility.
    #   6. Save data from each sheet as a table in the SQLite database.
    #   7. Commit the changes and close the database connection.
    # Parameters: None
    # Returns: None
    # Author: Aniket Pathare | 20050492@mydbs.ie
    # Precondition: The output directory should contain at least one Excel file, and the SQLite database path should be valid and accessible.
    # Date Created: 2024-11-17
    # ***************************************************************************************************************************************************************************************

    def save_to_sqlite(self):

        try:
            # Establish a connection to the SQLite database (creates the file if it doesn't exist)
            conn = sqlite3.connect(self.db_path)

            # Fetch all Excel files from the specified output directory
            excel_files = [
                os.path.join(self.output_dir, f)
                for f in os.listdir(self.output_dir)
                if f.endswith(".xlsx")
            ]

            # Check if there are no Excel files in the directory
            if not excel_files:
                print("No Excel files found in the output directory.")
                return

            # Identify the most recently modified Excel file
            latest_file = max(excel_files, key=os.path.getmtime)
            print(f"Processing the latest file: {latest_file}")

            # Load the latest Excel file and iterate over its sheets
            xls = pd.ExcelFile(latest_file)
            for sheet_name in xls.sheet_names:
                # Read data from the current sheet
                df = pd.read_excel(latest_file, sheet_name=sheet_name)

                # Clean up column names for compatibility with SQLite
                # Replace spaces and "+" symbols
                df.columns = [
                    str(col).replace(" ", "_").replace("+", "Plus")
                    for col in df.columns
                ]

                # Use the sheet name to create a table name for SQLite
                # Standardize table name
                table_name = sheet_name.replace(" ", "_").lower()

                # Save the data from the sheet to the SQLite database
                df.to_sql(table_name, conn, if_exists="replace", index=False)
                print(f"Data from sheet '{sheet_name}' saved to table '{table_name}'.")

            print("All data from the latest file saved to SQLite database successfully.")

            # Commit changes and close the database connection
            conn.commit()
            conn.close()

        except Exception as e:
            # Catch and print any errors that occur during the process
            print(f"An error occurred: {e}")

    # ***************************************************************************************************************************************************************************************
    # Function Name: integration_testing
    # Description: This function performs integration testing on an SQLite database by validating table existence, inspecting data integrity, and
    #              checking for null values and logical inconsistencies within the data.
    # Steps:
    #   1. Establish a connection to the SQLite database and retrieve all table names.
    #   2. Check if any tables exist in the database. If none, notify the user and exit.
    #   3. For each table:
    #       - Fetch the first 5 rows and display a sample of the data.
    #       - Check if the table contains any null values.
    #       - Perform logical checks on columns to determine if specific ones are numeric (e.g., "net_profit", "value").
    #   4. Summarize results for each table and highlight issues such as null values or non-numeric columns where numeric data is expected.
    #   5. Close the database connection after testing is completed.
    # Parameters: None
    # Returns: None
    # Author: Aniket Pathare | 20050492@mydbs.ie
    # Precondition: The database file should exist, and tables should contain data for meaningful testing. Column names must follow conventions
    #               (e.g., relevant numeric columns should be named accordingly).
    # Date Created: 2024-11-17
    # ***************************************************************************************************************************************************************************************

    def integration_testing(self):
        try:
            # Establish a connection to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Retrieve a list of all tables in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # If no tables are found, notify the user and exit
            if not tables:
                print("No tables found in the database.")
                return

            # Extract table names from the query result
            table_names = [table[0] for table in tables]
            print(f"Tables in the database: {table_names}")

            # Perform data integrity checks on each table
            for table in table_names:
                print(f"Checking data in table '{table}'")

                # Fetch the first 5 rows of data from the current table
                query = f"SELECT * FROM {table} LIMIT 5"
                try:
                    df = pd.read_sql_query(query, conn)
                except Exception as e:
                    print(f"Error while querying table '{table}': {e}")
                    continue

                # Check if the table is empty
                if df.empty:
                    print(f"Table '{table}' is empty.")
                else:
                    # Display a sample of the table's data
                    print(f"Sample data from table '{table}':\n{df.head()}")

                # Check for null values in the table
                if df.isnull().values.any():
                    print(f"Null values detected in table '{table}'.")
                else:
                    print(f"No null values detected in table '{table}'.")

                # Perform logical checks on specific columns
                for col in df.columns:
                    # Check if certain columns are numeric
                    if df[col].dtype == "object" and col.lower() in ["net_profit", "value"]:
                        try:
                            #Converting the column to float
                            df[col].astype(float)
                            print(f"Column '{col}' in table '{table}' is numeric.")
                        except ValueError:
                            print(f"Column '{col}' in table '{table}' is NOT numeric.")

            print("Integration testing completed successfully.")
            conn.close()

        except Exception as e:
            # Catch and print any errors that occur during the testing process
            print(f"An error occurred during testing: {e}")
