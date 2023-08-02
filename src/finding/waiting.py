
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


'''
Created on 1 ago. 2023

@author: jose-lopez
'''


def get_browser():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return browser


if __name__ == '__main__':

    driver = get_browser()

    driver.get("https://logeion.uchicago.edu/morpho/%E1%BC%80%CF%81%CE%B8%CE%AD%CE%BD%CF%84%CA%BC")

    try:
        h3_element_text = driver.find_element((By.TAG_NAME, "h3")).text
        print(h3_element_text)
        if WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Frequency")):
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "myDynamicElement"))
            )
    finally:
        driver.quit()
