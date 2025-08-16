import json
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from initialize_browser import InitializeBrowser
from Setuputility import SetupUtility
from robot.api.deco import keyword


from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
import os, time


driver=None
def load_locators(file_path):
    """Load locators from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def initialize_driver(device_type="web", browser="chrome"):
    """Initialize driver once for web or Android."""
    global driver
    # Remove quotes if they exist
    device_type = device_type.strip('"').strip("'")
    if device_type.lower() in ["android", "real_device", "emulator"]:
        driver = SetupUtility().connect_device(device_type=device_type)
    elif device_type.lower() == "web":
        driver = InitializeBrowser().initialize_browser(browser_name=browser)
    else:
        raise ValueError(f"Unsupported device type: {device_type}")
    return driver
    

def take_screenshot_on_error(message):
    """Takes a screenshot and logs it in Robot Framework report."""
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"screenshot_{timestamp}.png"
    screenshot_path = os.path.join(os.getcwd(), screenshot_name)

    if driver:
        driver.save_screenshot(screenshot_path)
        logger.error(message)  # Log error message
        logger.info(
            f'<a href="{screenshot_name}"><img src="{screenshot_name}" width="800px"></a>',
            html=True
        )
    else:
        logger.error("Driver not initialized, cannot take screenshot.")

def find_element(device_type, locator_dict, locator_key, timeout=10):
    """Find an element and handle failures with screenshot logging."""
    global driver
    try:
        if driver is None:
            initialize_driver(device_type)  # Make sure you have this implemented

        if locator_key not in locator_dict:
            raise KeyError(f"Locator '{locator_key}' not found in {locator_dict}")

        locator_all_keypairs = locator_dict[locator_key]
        
        by_type_andriod = {
            "id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "class_name": AppiumBy.CLASS_NAME,
            "android_ui_automator": AppiumBy.ANDROID_UIAUTOMATOR
        }
        by_type_web = {
            "id": By.ID,
            "xpath": By.XPATH,
            "xpath1": By.XPATH,
            "text": By.LINK_TEXT,
            "css": By.CSS_SELECTOR
        }
        by_type_choice=by_type_andriod if device_type.lower() in ["android", "real_device", 'emulator'] else by_type_web
        for loc_key, loc_value in locator_all_keypairs.items():
            value_of_choicen=by_type_choice.get(loc_key.lower())
            if value_of_choicen:
                try:
                    return driver.find_element(value_of_choicen, loc_value)
                except Exception:
                    continue 
    except Exception as e:
        take_screenshot_on_error(f"Error finding element '{locator_key}': {e}")
        raise e


@keyword
def go_to_url(url):
    """Navigate to the given URL using Selenium driver."""
    global driver
    if driver is None:
        raise Exception("Driver not initialized. Call 'Initialize Driver' first.")
    driver.get(url)


@keyword
def close_browser():
    global driver
    """Close the browser session."""
    if driver:
        driver.quit()
        driver = None
        
@keyword
def quit_driver():
        """Quit the driver if it's running."""
        global driver
        if driver:
            try:
                driver.quit()
                print("[INFO] Driver quit successfully.")
            except Exception as e:
                print(f"[ERROR] Error while quitting driver: {e}")
            finally:
                driver = None