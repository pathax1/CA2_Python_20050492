import pandas as pd

# ***************************************************************************************************************************************************************************************
# Function Name: load_test_data
# Description: This function loads test data from an Excel file and converts it into a list of dictionaries for use in data-driven testing.
# Steps:
#   1. Use the Pandas library to load the specified Excel sheet into a DataFrame.
#   2. Convert the DataFrame into a list of dictionaries where each row is represented as a dictionary.
#   3. Return the list of dictionaries for use in test cases.
#   4. If the file is not found, raise a FileNotFoundError with an appropriate message.
#   5. Handle any other exceptions that may occur during file processing and provide meaningful feedback to the user.
# Parameters:
#   - file_path: (str) The path to the Excel file containing the test data.
#   - sheet_name: (str) The name of the sheet within the Excel file to load.
# Returns:
#   - List of dictionaries representing the rows in the specified Excel sheet.
# Author: Aniket Pathare | 20050492@mydbs.ie
# Precondition: The specified Excel file must exist and the sheet_name parameter must match an existing sheet in the file.
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************
def load_test_data(file_path, sheet_name):
    try:
        # Load the data into a DataFrame
        test_data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Return data as a list of dictionaries
        return test_data.to_dict(orient='records')
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path {file_path} was not found.")
    except Exception as e:
        raise Exception(f"An error occurred while loading test data: {e}")
