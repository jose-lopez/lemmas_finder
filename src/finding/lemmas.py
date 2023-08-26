# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import quote
from os import path
from pathlib import Path
import os
import pandas as pd
from numpy.core.numeric import nan
import re

'''
Lemmas_finder: A python script to scrap lemmas from:
https://logeion.uchicago.edu/morpho/

Created on 21 jul. 2023

@authors: Jose Lopez, Jacobo Myerston

@email: josesmooth@gmail.com

@email: jmyerston@gmail.com
'''


def check_browser():

    print(f'Checking Google Chrome installation....' + "\n")

    with os.popen("google-chrome --version") as f1:
        browser = f1.readlines()

    if len(browser):

        print(f'Google Chrome is available: version: {browser[0]}' + "\n")

    else:

        print(f'Google Chrome is not available. Please install it as follows.' + "\n")

        print(f'wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb' + "\n")

        print(f'sudo apt install ./google-chrome-stable_current_amd64.deb' + "\n")

        exit(1)


def get_browser():

    options = webdriver.ChromeOptions()

    options.add_argument('--no-sandbox')

    options.add_argument('--disable-dev-shm-usage')

    options.add_argument("--headless=new")

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

        MSG = str(e)

        if MSG.startswith("No such driver version"):

            chrome_deb_url = "https://drive.google.com/file/d/1rw-T5jVOWuzhbbAmspLfzntt0xnJIuFe/view?usp=drive_link"

            print(f'Please, downgrade your chrome\'s version in order to find a Selenium\'s webdriver.' + "\n")

            print(f'This is a guide to follow: ' + "\n")

            print(f'Get an older and safe .deb chrome installer from here:' + "\n")

            print(f'{chrome_deb_url}' + "\n")

            print(f'Uninstall your current chrome\'s version this way:' + "\n")

            print(f'sudo apt-get purge --auto-remove google-chrome-stable' + "\n")

            print(f'For the installation you\'ll need sudo proviligies.' + "\n")

            print(f'sudo apt install ./google-chrome-stable_current_amd64.deb' + "\n")

            print(f'Finally, disable the automatic updates for chrome:' + "\n")

            print(f'sudo apt-mark hold google-chrome-stable' + "\n")

        else:

            print("An exception was raised whilst Selenium's webdriver was trying to open google-chrome." + "\n")
            print(e)

        exit(1)

    return browser


def get_best_lemma(frequency_elements: list) -> str:

    possible_lemmas = {}

    for element in frequency_elements:

        lemma = re.search("[\u1F00-\u1FFF\u0370-\u03FF\ʼ]+", element.text)

        frequency = re.search("[0-9]+", element.text)

        # Some frequency elements talks about unranked lemmas.
        unranked = re.search("unranked", element.text)

        if not unranked:  # If the lemma in the element is ranked,then it is added to the list of possible lemmas.

            if lemma and frequency:

                possible_lemmas[lemma.group()] = int(frequency.group())

        else:  # The lemma in the element is unranked,

            if len(frequency_elements) == 1:  # .. and the only one available, the lemma is useful.

                best_lemma = lemma.group()

    if possible_lemmas:

        sorted_lemmas = sorted(possible_lemmas.items(), key=lambda x: x[1], reverse=False)

        (best_lemma, _) = sorted_lemmas[0]

    return best_lemma


def get_lemma(browser, file, line, token, logs):

    url_base = "https://logeion.uchicago.edu/morpho/"

    url = url_base + quote(token)

    browser.get(url)  # navigate to URL

    # The number of "UL" html elements to wait for before getting lemmas and its frequencies.
    NUM_UL_ELEMENTS = 3

    # Setting how the waiting process must be done
    wait = WebDriverWait(browser, 20, poll_frequency=1, ignored_exceptions=[TimeoutException, NoSuchElementException])

    # For those unexpected or unknown html pages. This ensure we will know special tokens to debug.
    TRACKING_WAITS = 0

    # For those unexpected or unknown html pages. This ensure we will know special tokens to debug.
    WAITS = 1000  # Number or waiting steps (not seconds)

    try:

        stable_page = False

        while not stable_page:

            # Waiting until the Frequency field has some 'p' html elements.

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.ng-binding.ng-scope")))

            # -- Getting the HTML elements for the web scraping of lemmas and its frequencies. -- #

            md_content_element = browser.find_element(By.CSS_SELECTOR, "md-content.layout-padding._md")

            div_element = md_content_element.find_element(By.TAG_NAME, "div")

            ul_elements = div_element.find_elements(By.TAG_NAME, "ul")

            if not ul_elements:  # For those cases in which there aren't any lemmas and frequencies for the token.

                best_lemma = nan

                stable_page = True

            else:  # Here we have UL html elements to scrap.

                # print(f'The length of ul elements: {len(ul_elements)}    token: {token}')

                if len(ul_elements) == NUM_UL_ELEMENTS:

                    # The second of the ul_elements contains the lemmas and its frequencies.
                    frequency_elements = ul_elements[2].find_element(By.TAG_NAME, "li").find_elements(By.TAG_NAME, "p")

                    # Getting the best lemma for a token
                    best_lemma = get_best_lemma(frequency_elements)

                    stable_page = True

                else:

                    if TRACKING_WAITS == WAITS:

                        print(f'Special URL: Not enough UL html elements in File: {file} at line: {line}, token {token}' + "\n")
                        print(f'URL: {url}' + "\n")

                        logs.write(f'Special URL: Not enough UL html elements in File:: {file} at line: {line}, token {token}' + "\n")
                        logs.write(f'URL: {url}' + "\n")

                        best_lemma = nan

                        stable_page = True

                    else:

                        TRACKING_WAITS += 1

    except NoSuchElementException:

        lemma = nan

        print(f'Getting not Frequencies error: An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")

        logs.write(f'Getting not Frequencies error: An exception of type NoSuchElementException in File: {file} at line: {line}, token {token}' + "\n")
        logs.write(f'URL: {url}' + "\n")

    except TimeoutException:

        lemma = nan

        print(f'Getting URL error: An exception of type TimeoutException in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")

        logs.write(f'Getting URL error: An exception of type TimeoutException in File: {file} at line: {line}, token {token}' + "\n")
        logs.write(f'URL: {url}' + "\n")

    except Exception:

        lemma = nan

        print(f'Getting URL error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
        print(f'URL: {url}' + "\n")

        logs.write(f'Getting URL error: A non anticipated exception in File: {file} at line: {line}, token {token}' + "\n")
        logs.write(f'URL: {url}' + "\n")

    else:

        try:

            browser.find_element(By.XPATH, "//*[contains(text(), 'Could not find the search term')]")

            lemma = nan

        except NoSuchElementException:

            try:

                browser.find_element(By.XPATH, "//*[contains(text(), 'Morpho cannot find the form you a searching for')]")

                lemma = nan

            except NoSuchElementException:

                lemma = best_lemma

    finally:

        return lemma


def check_token(token):

    warning = False

    invalid_token = re.search("[^\u1F00-\u1FFF\u0370-\u03FF\.',;·ʼ]", token)

    if invalid_token:

        warning = True

    return warning


if __name__ == '__main__':

    print("\n" + f'Lemmas_finder: A python script to scrap lemmas from logeion.uchicago.edu/morpho/' + "\n")

    check_browser()

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

        processed_file = root + folders[0] + file_root_name + "_processed.csv"

        new_lemmas_file = root + folders[0] + file_root_name + "_new_lemmas.csv"

        warnings_file = root + folders[1] + file_root_name + "_warnings" + ".csv"

        logs_file = root + folders[2] + file_root_name + "_logs" + ".csv"

        logs = open(
            logs_file, 'w', encoding="utf8")

        warnings_in_file = []

        new_lemmas_in_file = []

        input_df = pd.read_csv(file)

        print(f'Getting lemmas for {file} file: {processed_files} | {files_to_process}' + "\n")

        for x in input_df.index:

            token = input_df.loc[x, "token"]

            lemma = input_df.loc[x, "lemma"]

            warning = check_token(token)

            if warning:

                warnings_in_file.append([x, token])

            if lemma is nan:

                lemma = get_lemma(browser, file, x, token, logs)

                print(f'Token {token}       lemma : {lemma}')

                new_lemmas_in_file.append([x, token, lemma])

                input_df.loc[x, "lemma"] = lemma

        input_df.to_csv(processed_file)

        # Building the warnings' file, if there are any, for the file on process.

        if len(warnings_in_file) != 0:

            print(f'Warnings found for {file} file. A report in {warnings_file}')

            warnings_df = pd.DataFrame(warnings_in_file, columns=['line', 'token'])

            warnings_df.to_csv(warnings_file)

        new_lemmas_in_file_df = pd.DataFrame(new_lemmas_in_file, columns=['line', 'token', 'lemma'])

        new_lemmas_in_file_df.to_csv(new_lemmas_file)

        logs.close()

    browser.close()

    print(f'..... done')
