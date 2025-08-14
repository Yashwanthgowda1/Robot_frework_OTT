import os
import json
import socket
import time
import subprocess
from collections import OrderedDict
from appium import webdriver
from appium.options.android import UiAutomator2Options
from robot.api.deco import keyword

# Path to config.json (kept in project folder)
CONFIG_PATH = r"C:\\python_study\\OTT\\Robot_frework_OTT\\config.json"

class SetupUtility:
    def __init__(self):
        self.driver = None

    @keyword("Connect Device")
    def connect_device(self, device_type):
        """Connects to Web or Android device based on config.json settings."""
        config_data = self.load_config()

        if device_type not in config_data:
            raise ValueError(f"Device '{device_type}' not found in config.json")

        device_config = config_data[device_type]
        port = device_config["port"]

        # Start Appium server for this device
        self.start_appium_server(port)

        # Remove 'port' key from desired capabilities
        caps = {k: v for k, v in device_config.items() if k != "port"}

        appium_server = f"http://localhost:{port}/wd/hub"

        print(f"\n[INFO] Connecting to {device_type} at {appium_server}")
        print("[INFO] Desired Capabilities:", caps)

        # ✅ Use UiAutomator2Options for Android
        options = UiAutomator2Options().load_capabilities(caps)

        driver = webdriver.Remote(
            command_executor=appium_server,
            options=options
        )

        self.driver = driver
        print(f"[INFO] Connected to {device_config.get('name', 'device')}")
        return driver

    def load_config(self):
        """Loads config.json into a dictionary."""
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

        with open(CONFIG_PATH, 'r') as file:
            config = json.load(file, object_pairs_hook=OrderedDict)

        print(f"[INFO] Loaded configuration from {CONFIG_PATH}")
        return config

    def is_port_in_use(self, port):
        """Checks if a given port is already in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    def start_appium_server(self, port):
        """Starts Appium server on given port."""
        if self.is_port_in_use(port):
            print(f"[WARNING] Port {port} in use. Killing process...")
            os.system("taskkill /F /IM node.exe")
            time.sleep(2)

        print(f"[INFO] Starting Appium server on port {port}...")
        subprocess.Popen(
            ["appium", "-p", str(port), "--allow-insecure", "chromedriver_autodownload"],
            shell=True
        )
        time.sleep(8)  # Wait for server to start
        print(f"[INFO] Appium server started at http://localhost:{port}")


if __name__ == "__main__":
    setup_util = SetupUtility()
    driver = setup_util.connect_device("emulator")
