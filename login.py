import pathlib

import time
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

import os
import shutil

def login_chrome():
    # Define the folder path
    folder_path = "chrome-data"

      # # Check if the folder exists
      # if os.path.exists(folder_path):
      #   print(f"Deleting folder '{folder_path}' and its contents...")
      #   try:
      #     # Use shutil.rmtree for recursive deletion
      #     shutil.rmtree(folder_path)
      #     print("Deletion successful!")
      #   except OSError as e:
      #     print(f"Error deleting folder: {e}")
      # else:
      #   print(f"Folder '{folder_path}' does not exist. New will be created")


    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")
    script_directory = pathlib.Path().absolute()
    chrome_options.add_argument(f"--user-data-dir={script_directory}\\chrome-data")

    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
    })

    driver = uc.Chrome(options=chrome_options)

    driver.get("https://google.com")
    # time.sleep(10)
    sign_in = driver.find_elements(By.XPATH, "//a[@class='gb_Da gb_nd gb_Pd gb_ne']")
    sign_in_2 = driver.find_elements(By.XPATH, "//a[contains(@href,'accounts.google.com/ServiceLogin')]")
    sign_in_3= driver.find_elements(By.XPATH, "//a[@aria-label='Sign in']")

    print(sign_in_3)
    print(sign_in)
    print(sign_in_2)

    time.sleep(100)

    # input("Please sign in and press enter here in the terminal: ")

    driver.close()
