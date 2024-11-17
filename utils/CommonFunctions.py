
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def highlight_element(driver, element, color="red", border_width="3px"):
    """
    Highlights a Selenium WebElement by applying a border style.
    """
    original_style = element.get_attribute("style")
    highlight_style = f"border: {border_width} solid {color};"

    # Apply highlight
    driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, highlight_style)

    # Revert back to original style after a brief pause
    import time
    time.sleep(0.5)
    driver.execute_script(f"arguments[0].setAttribute('style', arguments[1]);", element, original_style)


def iaction(driver, element, identifywith, iProperty, ivalue=None):
    """
    Perform an action based on the element type, identification method, and value.
    """
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
