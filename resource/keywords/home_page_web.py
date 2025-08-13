from resource.library.common_web_andriod import *
from selenium.webdriver.support import WebDriverWait

from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

setting_dict = load_locators("locators/setting_page.json")

def click_on_setting_icon_click_on_sing_in():
    """Click on the setting icon and then click on the sign-in button."""
    find_element("web", setting_dict, "setting_icon").click()