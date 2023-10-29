from time import sleep
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(
        color_scheme='dark',


    )
    page = context.new_page()


    page.goto('http://dgg.gg')

    print(page.title())
    browser.close()