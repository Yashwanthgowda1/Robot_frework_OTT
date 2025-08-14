import json
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, KeyError, ValueError
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
    if device_type.lower() in ["android", "real_device", 'emulator']:
        driver = SetupUtility().connect_device(device_type=device_type)
    elif device_type.lower() == "web":
        driver = InitializeBrowser().initialize_browser(browser_name=browser)
    else:
        raise ValueError(f"Unsupported device type: {device_type}")
    return driver
    
driver = None

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

        locator = locator_dict[locator_key]
        loc_type = locator[0]
        loc_value = locator[1]

        loc_type_lower = loc_type.lower()
        by_type = {
            "id": AppiumBy.ID,
            "xpath": AppiumBy.XPATH,
            "accessibility_id": AppiumBy.ACCESSIBILITY_ID,
            "class_name": AppiumBy.CLASS_NAME,
            "android_ui_automator": AppiumBy.ANDROID_UIAUTOMATOR
        }.get(loc_type_lower)

        if not by_type:
            raise ValueError(f"Unsupported locator type: {loc_type_lower}")

        return driver.find_element(by_type, loc_value)

    except (NoSuchElementException, TimeoutException, KeyError, ValueError) as e:
        take_screenshot_on_error(f"Error finding element '{locator_key}': {str(e)}")
        raise e 

