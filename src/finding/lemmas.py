# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver   # for webdriver
# from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from urllib.parse import quote
from os import path
from pathlib import Path
import os


'''
Created on 21 jul. 2023

@author: jose-lopez

'''


def get_lemma(word, browser, url_base):

    url = url_base + quote(word)

    browser.get(url)

    browser.implicitly_wait(0.5)

    content = browser.page_source

    parser = BeautifulSoup(content, "lxml")

    tag = parser.find_all('h1', class_='ng-binding')

    print(tag)


if __name__ == '__main__':

    folders = ["processed", "temp"]

    root = "./texts/"
    corpus = root + "corpus"

    processed_files = 0

    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)

    for folder in folders:
        _path = root + folder
        if not path.exists(_path):
            os.mkdir(_path)

    files = [str(x) for x in Path(corpus).glob("**/*.txt")]

    for file in files:

        processed_files += 1

        with open(file, 'r', encoding="utf8") as f:
            lines = f.readlines()

    browser.close()

    browser.quit()
