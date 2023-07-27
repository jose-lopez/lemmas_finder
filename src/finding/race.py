import nest_asyncio
from playwright.sync_api import sync_playwright

nest_asyncio.apply()

pw = sync_playwright.start()
chrome = pw.chromium.launch(headless=False)
page = chrome.new_page()
page.goto("https://twitch.tv")

