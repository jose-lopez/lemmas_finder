# selenium 4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

'''
Created on 1 ago. 2023

@author: jose-lopez
'''


def get_driver():

    """ Setting the driver with some convenient options """

    # getting the webdriver's path

    # webdriver_p = ChromeDriverManager(path='./chromedriver', log_level=0).install() # Setting a clean output in the terminal

    options = Options()

    user_agent = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

    options.add_argument(f'user-agent={user_agent}')

    options.add_argument("--disable-web-security")

    options.add_argument("--disable-extensions")

    options.add_argument("--disable-notifications")

    options.add_argument("--disable-web-security")

    options.add_argument("--ignore-certificate-errors")

    options.add_argument("--no-sandbox")

    options.add_argument("--allow-running-insecure-content")

    options.add_argument("--no-default-browser-check")

    options.add_argument("--no-first-run")

    options.add_argument("--no-proxy-server")

    options.add_argument("--disable-blink-features=AutomationController")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # s = Service(webdriver_p)

    # driver = webdriver.Chrome(service=s, options=options)

    return browser


if __name__ == '__main__':

    browser = get_driver()

    print("Plase press Enter to continue")

    browser.quit()
