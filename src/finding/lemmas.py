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


def get_browser():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")

    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    return browser


def get_lemma(file, line, token, browser, logs):

    url_base = "https://logeion.uchicago.edu/morpho/"

    url = url_base + quote(token)

    browser.get(url)  # navigate to URL

    # time.sleep(5)    # to retrieve full and stable rendered HTML content

    # condition_element = browser.find_element(By.TAG_NAME, "h3").text

    # print(condition_element)

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

        # print(lemma)

        invalid_lemma = re.search("[^\u1F00-\u1FFF\u0370-\u03FF\]+", lemma)

        if invalid_lemma:

            lemma = nan

    finally:

        return lemma


def check_errors(token: str, lemma: str):

    error = None

    invalid_token = re.search("[^\u1F00-\u1FFF\u0370-\u03FF\]+", token)

    if lemma is not nan:

        invalid_lemma = re.search("[^\u1F00-\u1FFF\u0370-\u03FF\]+", lemma)

    else:

        invalid_lemma = False

    if invalid_token and not invalid_lemma:

        error = 1

    if not invalid_token and invalid_lemma:

        error = 2

    if invalid_token and invalid_lemma:

        error = 3

    return error


if __name__ == '__main__':

    folders = ['processed', 'errors', 'logs']

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

    errors_in_file = []

    for file in files:

        file_name = "/" + file.split("/")[-1]

        processed_files += 1

        processed_file = root + folder[0] + file_name

        errors_file = root + folder[1] + file_name

        logs_file = root + folder[2] + file_name

        logs = open(
            logs_file, 'w', encoding="utf8")

        input_df = pd.read_csv(file)

        # print(df.to_string())

        print(f'Getting lemmas for {file_name} file: {processed_files} | {files_to_process}')

        for x in input_df.index:

            token = input_df.loc[x, "token"]

            lemma = input_df.loc[x, "lemma"]

            error = check_errors(token, lemma)

            if not error:

                lemma = get_lemma(browser, file, x, token, logs)

                print(f'token = {input_df.loc[x, "token"]}   lemma = {input_df.loc[x, "lemma"]}' + "\n")

                input_df.loc[x, "lemma"] = lemma

            else:

                errors_in_file.append([x, token, lemma, error])

        input_df.to_csv(processed_file)

        # Building the error's file, if there are any, for the actual file in process,

        if len(errors_in_file):

            print(f'Errors found in {file_name} file. A report in {errors_file}')

            errors_df = pd.DataFrame(errors_in_file, columns=['line', 'token', 'lemma', 'error_type'])

            errors_df.to_csv(errors_file)

        logs.close()

    print(f'..... done')
