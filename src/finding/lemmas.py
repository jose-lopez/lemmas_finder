# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from urllib.parse import quote
from os import path
from pathlib import Path
import os
import pandas as pd
from numpy.core.numeric import nan
import re


'''
Created on 21 jul. 2023

@author: jose-lopez

'''


def install_browser():

    with os.popen("google-chrome --version") as f:
        browser = f.readlines()

    if len(browser):

        print(f'Google Chrome version: {browser[0]}' + "\n")

    else:

        print(f'... Installinng Google Chrome' + "\n")

        try:

            print(os.popen('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb').read())
            print(os.popen('apt install ./google-chrome-stable_current_amd64.deb').read())

        except Exception as exc:

            print(exc)


def get_browser():

    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument('--no-sandbox')

    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return browser


def get_lemma(browser, file, line, token, logs):

    url_base = "https://logeion.uchicago.edu/morpho/"

    url = url_base + quote(token)

    browser.get(url)  # navigate to URL

    try:

        # Waiting for a totally deployed URL.

        WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Short Definition"))

    except NoSuchElementException:

        lemma = nan

        logs.write(f'An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")

    except TimeoutException:

        lemma = nan

        logs.write(f'An exception of type TimeoutException in File: {file} at line: {line}, token {token}' + "\n")

    else:

        lemma = browser.find_element(By.CSS_SELECTOR, 'a.ng-binding').text

        invalid_lemma = re.search(r'[a-zA-Z0-9]+', lemma)

        if invalid_lemma:

            lemma = nan

    finally:

        return lemma


def check_warning(token, lemma):

    warning = None

    invalid_token = re.search(r'[a-zA-Z0-9]+', token)

    if lemma is not nan:

        invalid_lemma = re.search(r'[a-zA-Z0-9]+', lemma)

    else:

        invalid_lemma = None

    if invalid_token and not invalid_lemma:

        warning = 1

    if not invalid_token and invalid_lemma:

        warning = 2

    if invalid_token and invalid_lemma:

        warning = 3

    return warning


if __name__ == '__main__':

    install_browser()

    folders = ['processed', 'warnings', 'logs']

    root = "./text/"
    corpus = root + "corpus"

    for folder in folders:
        _path = root + folder
        if not path.exists(_path):
            os.mkdir(_path)

    processed_files = 0

    browser = get_browser()

    files = [str(x) for x in Path(corpus).glob("**/*.csv")]

    files_to_process = len(files)

    warnings_in_file = []

    for file in files:

        file_name = "/" + file.split("/")[-1]

        file_root_name = file_name.split(".")[0]

        processed_files += 1

        processed_file = root + folders[0] + file_name

        warnings_file = root + folders[1] + file_root_name + "_warnings" + ".csv"

        logs_file = root + folders[2] + file_root_name + "_logs" + ".csv"

        logs = open(
            logs_file, 'w', encoding="utf8")

        input_df = pd.read_csv(file)

        print(f'Getting lemmas for {file} file: {processed_files} | {files_to_process}' + "\n")

        for x in input_df.index:

            token = input_df.loc[x, "token"]

            lemma = input_df.loc[x, "lemma"]

            warning = check_warning(token, lemma)

            if warning:

                warnings_in_file.append([x, token, lemma, warning])

            if lemma is nan:

                lemma = get_lemma(browser, file, x, token, logs)

                print(f'token = {token}   lemma = {lemma}' + "\n")

                input_df.loc[x, "lemma"] = lemma

        input_df.to_csv(processed_file)

        # Building the warnings' file, if there are any, for the actual file in process.

        if len(warnings_in_file) != 0:

            print(f'Warnings found for {file} file. A report in {warnings_file}')

            warnings_df = pd.DataFrame(warnings_in_file, columns=['line', 'token', 'lemma', 'error_type'])

            warnings_df.to_csv(warnings_file)

        logs.close()

    print(f'..... done')
