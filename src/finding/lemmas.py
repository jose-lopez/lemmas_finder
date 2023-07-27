# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
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


def get_lemma(token, browser):

    url_base = "https://logeion.uchicago.edu/"

    url = url_base + quote(token)

    browser.get(url)  # navigate to URL

    time.sleep(0.5)    # to retrieve full and stable rendered HTML content

    content = browser.page_source

    parser = BeautifulSoup(content, "html.parser")

    tag = parser.find('h1', class_='ng-binding')

    lemma = tag.text

    return lemma


if __name__ == '__main__':

    folders = ["processed"]  # Maybe, in the future, we need other folders.

    root = "./text/"
    corpus = root + "corpus"
    processed_root = root + "processed/"

    for folder in folders:
        _path = root + folder
        if not path.exists(_path):
            os.mkdir(_path)

    processed_files = 0

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    files = [str(x) for x in Path(corpus).glob("**/*.csv")]

    for file in files:

        file_name = file.split("/")[-1]

        processed_files += 1

        processed_file = processed_root + file_name

        df = pd.read_csv(file)

        # print(df.to_string())

        for x in df.index:

            if df.loc[x, "lemma"] is nan:

                lemma = get_lemma(df.loc[x, "token"], browser)

                print(f'token = {df.loc[x, "token"]}   lemma = {lemma}' + "\n")

                if lemma is not nan:

                    df.loc[x, "lemma"] = lemma.strip()

                else:

                    df.loc[x, "lemma"] = nan

        df.to_csv(processed_file)


