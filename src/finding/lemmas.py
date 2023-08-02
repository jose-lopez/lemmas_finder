# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
from os import path
from pathlib import Path
import os
import pandas as pd
from numpy.core.numeric import nan
import time


'''
Created on 21 jul. 2023

@author: jose-lopez

'''


def get_browser():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return browser


def get_lemma(token, browser):

    url_base = "https://logeion.uchicago.edu/morpho/"

    url = url_base + quote(token)

    browser.get(url)  # navigate to URL

    # time.sleep(5)    # to retrieve full and stable rendered HTML content

    # condition_element = browser.find_element(By.TAG_NAME, "h3").text

    # print(condition_element)

    if WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Short Definition")):

        lemma = browser.find_element(By.CSS_SELECTOR, 'a.ng-binding').text

        # print(lemma)

        if lemma.startswith("Search corpus for this form only"):

            lemma = nan

        return lemma


if __name__ == '__main__':

    root = "./text/"
    corpus = root + "corpus"
    processed_path = root + "processed/"

    if not path.exists(processed_path):
        os.mkdir(processed_path)

    processed_files = 0

    browser = get_browser()

    files = [str(x) for x in Path(corpus).glob("**/*.csv")]

    for file in files:

        file_name = file.split("/")[-1]

        processed_files += 1

        processed_file = processed_path + file_name

        df = pd.read_csv(file)

        # print(df.to_string())

        for x in df.index:

            if df.loc[x, "lemma"] is nan:

                lemma = get_lemma(df.loc[x, "token"], browser)

                df.loc[x, "lemma"] = lemma

            print(f'token = {df.loc[x, "token"]}   lemma = {df.loc[x, "lemma"]}' + "\n")

        df.to_csv(processed_file)
