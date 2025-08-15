import json
import os
import subprocess
import time
import socket
from collections import OrderedDict
from appium import webdriver


class SetupUtility:
    def __init__(self, config_path=r"D:\ROBOT_FRAMEWORK\config.json"):
        self.config_path = config_path
        self.driver = None

    def is_port_in_use(self, port):
        """Check if a given TCP port is already in use."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    def load_config(self):
        """Load JSON config from file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file {self.config_path} not found")
        with open(self.config_path, 'r') as file:
            config = json.loads(file.read(), object_pairs_hook=OrderedDict)
            print(f"[INFO] Loaded configuration from {self.config_path}")
            return config

    def start_appium_server(self, port):
        """Start Appium server on the given port."""
        if self.is_port_in_use(port):
            print(f"[WARNING] Port {port} already in use. Killing process...")
            os.system("taskkill /F /IM node.exe")
            time.sleep(2)
        print(f"[INFO] Starting Appium server on port {port}...")
        subprocess.Popen(
            ["appium", "-p", str(port), "--allow-insecure", "chromedriver_autodownload"],
            shell=True
        )
        time.sleep(8) 
        print(f"[INFO] Appium server started at http://localhost:{port}")

    def connect_device(self, device_type):
        """Connect to the given device type."""
        config_data = self.load_config()
        if device_type not in config_data:
            raise ValueError(f"Device type '{device_type}' not found in config.json")
        device_config = config_data[device_type]
        port = device_config["port"]
        self.start_appium_server(port)
        caps = {k: v for k, v in device_config.items() if k != "port"}
        appium_server = f"http://localhost:{port}"
        print(f"\n[INFO] Connecting to {device_type} on {appium_server}")
        print("[INFO] Desired Capabilities:")
        for k, v in caps.items():
            print(f"  {k}: {v}")
        self.driver = webdriver.Remote(
            command_executor=appium_server,
            desired_capabilities=caps
        )
        print(f"[INFO] Successfully connected to {device_config['name']}")
        return self.driver

    def quit_driver(self):
        """Quit the driver if it's running."""
        if self.driver:
            try:
                self.driver.quit()
                print("[INFO] Driver quit successfully.")
            except Exception as e:
                print(f"[ERROR] Error while quitting driver: {e}")
            finally:
                self.driver = None


if __name__ == "__main__":
    setup_util = SetupUtility()
    driver = None
    try:
        driver = setup_util.connect_device("emulator")  # Change as needed
        time.sleep(3)
    except Exception as e:
        print("[ERROR]", e)
    finally:
        setup_util.quit_driver()
