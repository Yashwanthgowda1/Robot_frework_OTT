import json
from selenium.webdriver.common.by import By
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from initialize_browser import InitializeBrowser
from Setuputility import SetupUtility
from robot.api.deco import keyword

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
    
@keyword("Find Element")
def find_element(device_type, loactor_dict, locator_key, timeout=10):
        """Find an element using the specified locator."""
        global driver
        if driver is None:
            initialize_driver(device_type)
        if locator_key not in loactor_dict:
            raise KeyError(f"Locator '{locator_key}' not found in {loactor_dict}")
        locator = loactor_dict[locator_key]
        my_dict={
            "id": AppiumBy.ID if device_type.lower() in ["android", "real_device","emulator"] else By.ID,
            "xpath": AppiumBy.XPATH if device_type.lower() in ["android", "real_device", "emulator"] else By.XPATH,
            "xpath1": AppiumBy.XPATH if device_type.lower() in ["android", "real_device", "emulator"] else By.XPATH,  # same as xpath
            "css": None if device_type.lower() in ["android", "real_device","emulator"] else By.CSS_SELECTOR,
            "name": None if device_type.lower() in ["android", "real_device", "emulator"] else By.NAME,
            "text": AppiumBy.ANDROID_UIAUTOMATOR if device_type.lower() in ["android", "real_device", "emulator"] else None,
            "content-desc": AppiumBy.ACCESSIBILITY_ID if device_type.lower() in ["android", "real_device", "emulator"] else None
        }
        for loc_type_lower,  loc_value in locator.items():
            if  my_dict[loc_type_lower] and loc_value:
                if loc_type_lower == "text" and device_type.lower() in ["android", "real_device"]:
                    loc_value = f'new UiSelector().text("{loc_value}")'
                return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((my_dict[loc_type_lower], loc_value)))
            raise ValueError(f"Unsupported locator type: {loc_type_lower}")

