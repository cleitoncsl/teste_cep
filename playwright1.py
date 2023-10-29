import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto('http://dgg.gg')

    print(page.title())

    browser.close()