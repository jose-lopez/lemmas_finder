from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from urllib.parse import quote
from os import path
from pathlib import Path
import os
import pandas as pd
from numpy.core.numeric import nan
import re
import logging

'''
Created on 1 ago. 2023

@author: jose-lopez
'''


def get_browser():

    options = webdriver.ChromeOptions()

    options.add_argument('--no-sandbox')

    options.add_argument('--disable-dev-shm-usage')

    # options.add_argument("--headless=new")

    options.add_argument("--disable-web-security")

    options.add_argument("--disable-extensions")

    options.add_argument("--disable-notifications")

    options.add_argument("--ignore-certificate-errors")

    options.add_argument("--allow-running-insecure-content")

    options.add_argument("--no-default-browser-check")

    options.add_argument("--no-first-run")

    options.add_argument("--no-proxy-server")

    options.add_argument("--disable-blink-features=AutomationController")

    try:

        browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    except Exception as e:

        print("An exception was raised whilst Selenium's webdriver was trying to open google-chrome.")
        print(e)

        exit(1)

    return browser


if __name__ == '__main__':

    DEMO_PAGE = '''
        <html>
         <body>
          <form id="loginForm">
           <input name="username" type="text" />
           <input name="password" type="password" />
           <input name="continue" type="submit" value="Login" />
           <input name="continue" type="button" value="Clear" />
          </form>
        </body>
        </html>
        '''

    driver = get_browser()

    driver.get(DEMO_PAGE)

    login_form = driver.find_element(By.XPATH, "/html/body/form[1]")

    driver.close
