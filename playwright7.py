from time import sleep
from playwright.sync_api import sync_playwright

url = 'https://selenium.dunossauro.live/aula_05_a.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        color_scheme='dark'
    )

    page = context.new_page()
    page.goto(url)

    locator = page.locator('div')
    result = locator.nth(0).text_content()

    print(result)

    sleep(1)
    browser.close()