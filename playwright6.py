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

    div1 = page.locator('xpath=//*[@id="python"]')  # XPATH
    div2 = page.locator('#python')  # CSS


    print(div1.text_content())
    print('--------------')
    print(div2.text_content())

    div3 = page.locator('id=python')  # CSS
    print(div3.text_content())  # PW


    h2 = page.locator('#python > h2')
    print(h2.text_content())





    sleep(1)
    browser.close()