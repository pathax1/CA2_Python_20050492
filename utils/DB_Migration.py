import sqlite3
import pandas as pd
import os


class DBMigration:
    """
    A class to handle data migration from Excel files to an SQLite database and perform integration testing.
    """

    def __init__(self, output_dir, db_path="data_analysis.db"):
        """
        Initialize the DBMigration class.

        Parameters:
        - output_dir: Directory containing the Excel files.
        - db_path: Path to the SQLite database file.
        """
        self.output_dir = output_dir  # Directory where Excel files are stored
        self.db_path = db_path  # Path to the SQLite database file

    def save_to_sqlite(self):
        """
        Saves the extracted data from the latest Excel file in the output directory into an SQLite database.
        """
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
                df.columns = [
                    str(col).replace(" ", "_").replace("+", "Plus")  # Replace spaces and "+" symbols
                    for col in df.columns
                ]

                # Use the sheet name to create a table name for SQLite
                table_name = sheet_name.replace(" ", "_").lower()  # Standardize table name

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

    def integration_testing(self):
        """
        Performs integration testing on the SQLite database.
        """
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
                            df[col].astype(float)  # Try converting the column to float
                            print(f"Column '{col}' in table '{table}' is numeric.")
                        except ValueError:
                            print(f"Column '{col}' in table '{table}' is NOT numeric.")

            print("Integration testing completed successfully.")
            conn.close()

        except Exception as e:
            # Catch and print any errors that occur during the testing process
            print(f"An error occurred during testing: {e}")
