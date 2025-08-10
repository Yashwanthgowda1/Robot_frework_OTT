import json
import os
import subprocess
import time
from collections import OrderedDict
from appium import webdriver
import socket

file_path = r"D:\\ROBOT_FRAMEWORK\\config.json"

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def load_config(config_file=file_path):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file {config_file} not found")
    with open(config_file, 'r') as file:
        config = json.loads(file.read(), object_pairs_hook=OrderedDict)
        print(f"[INFO] Loaded configuration from {config_file}")
        return config

def start_appium_server(port):
    if is_port_in_use(port):
        print(f"[WARNING] Port {port} already in use. Killing process...")
        os.system("taskkill /F /IM node.exe")
        time.sleep(2)
    print(f"[INFO] Starting Appium server on port {port}...")
    subprocess.Popen(
        ["appium", "-p", str(port), "--allow-insecure", "chromedriver_autodownload"],
        shell=True
    )
    time.sleep(8)  # Wait more to ensure Appium is ready
    print(f"[INFO] Appium server started at http://localhost:{port}")

def connect_device(device_type):
    config_data = load_config()
    if device_type not in config_data:
        raise ValueError(f"Device type '{device_type}' not found in config.json")
    device_config = config_data[device_type]
    port = device_config["port"]
    start_appium_server(port)
    caps = {k: v for k, v in device_config.items() if k != "port"}
    appium_server = f"http://localhost:{port}"
    print(f"\n[INFO] Connecting to {device_type} on {appium_server}")
    print("[INFO] Desired Capabilities:")
    for k, v in caps.items():
        print(f"  {k}: {v}")
    driver = webdriver.Remote(command_executor=appium_server,desired_capabilities=caps
)

    print(f"[INFO] Successfully connected to {device_config['name']}")
    return driver


try:
    driver = connect_device("emulator")
    time.sleep(3)
except Exception as e:
        print("[ERROR]", e)
finally:
        if driver:
            driver.quit()
