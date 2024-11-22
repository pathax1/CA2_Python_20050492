# ***************************************************************************************************************************************************************************************
# Function Names: highlight_element,iaction
# Description: These functions are used to enhance the execution
# Parameters: driver,element,colour,border_width,identifywith,iProperty,ivalue
# Author:Aniket Pathare | 20050492@mydbs.ie
# Precondition: User should be entering valid element identifier to proceed
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
from datetime import datetime
import pandas as pd

# ***************************************************************************************************************************************************************************************
# Function Names:highlight_element
# Description:This function is used for highlighting the webelement on which the action or event is going to happen
# Parameters:driver,element,colour,border_width
# Author:Aniket Pathare | 20050492@mydbs.ie
# Precondition:Element which needs to be highlighted a valid element identifier should be passed
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************
def highlight_element(driver, element, color="red", border_width="3px"):

    original_style = element.get_attribute("style")
    highlight_style = f"border: {border_width} solid {color};"

    # Apply highlight
    driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, highlight_style)

    # Revert back to original style after a brief pause
    import time
    time.sleep(0.5)
    driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, original_style)

# ***************************************************************************************************************************************************************************************
# Function Names:iaction
# Description:This function is used for identifying the element using multiple parameters
# Parameters:driver,element,colour,border_width
# Author:Aniket Pathare | 20050492@mydbs.ie
# Precondition:Element which needs to be highlighted a valid element identifier should be passed
# Date Created: 2024-11-17
# ***************************************************************************************************************************************************************************************
def iaction(driver, element, identifywith, iProperty, ivalue=None):

    # Define locator mapping
    locate_by = {
        "XPATH": By.XPATH,
        "CSS_SELECTOR": By.CSS_SELECTOR,
        "ID": By.ID,
        "NAME": By.NAME,
        "CLASS_NAME": By.CLASS_NAME,
        "TAG_NAME": By.TAG_NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
    }

    # Validate the locator method
    if identifywith not in locate_by:
        return f"Invalid identification method: {identifywith}"

    # Get the Selenium locator strategy
    by = locate_by[identifywith]

    try:
        match element:
            case "Textbox":
                # Wait for the element and send input
                textbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, iProperty)))
                highlight_element(driver, textbox)
                print(ivalue)
                textbox.send_keys(ivalue)
                return f"Text entered in Textbox using {identifywith}: {ivalue}"

            case "Button":
                # Wait for the button and click it
                button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, iProperty)))
                highlight_element(driver, button)
                button.click()
                return f"Button clicked using {identifywith}"

            case "Radio Button":
                # Wait for the radio button and select it
                radio_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, iProperty)))
                highlight_element(driver, radio_button)
                radio_button.click()
                return f"Radio Button selected using {identifywith}"

            case "Checkbox":
                # Wait for the checkbox and toggle it
                checkbox = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, iProperty)))
                highlight_element(driver, checkbox)
                if not checkbox.is_selected():
                    checkbox.click()
                return f"Checkbox toggled using {identifywith}"

            case "Hyperlink":
                # Wait for the hyperlink and click it
                hyperlink = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, iProperty)))
                highlight_element(driver, hyperlink)
                hyperlink.click()
                return f"Hyperlink clicked using {identifywith}"

            case "Image":
                # Wait for the image to load
                image = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((by, iProperty)))
                highlight_element(driver, image)
                return f"Image loaded using {identifywith}"

            case _:
                return f"Invalid element type: {element}"

    except Exception as e:
        return f"Error performing action on {element} using {identifywith}: {str(e)}"
