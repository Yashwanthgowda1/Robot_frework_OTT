from selenium import webdriver


class InitializeBrowser:
    def __init__(self):
        self.driver = None


    def initialize_browser(self, browser_name="chrome"):
        """Initialize a browser session."""
        browser_name = browser_name.lower()
        if browser_name == "chrome":
            self.driver = webdriver.Chrome()
        elif browser_name == "firefox":
            self.driver = webdriver.Firefox()
        elif browser_name == "edge":
            self.driver = webdriver.Edge()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        self.driver.maximize_window()
        return self.driver



    # @keyword

 
    # def go_to(self, url):
    #     if self.driver is None:
    #         raise Exception("Browser is not initialized. Call 'Initialize Browser' first.")
    #     self.driver.get(url)


    # @keyword
    # def close_browser(self):
    #     """Close the browser session."""
    #     if self.driver:
    #         self.driver.quit()
    #         self.driver = None
