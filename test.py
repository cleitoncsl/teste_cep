import re
from time import sleep
from playwright.sync_api import expect, sync_playwright

url = 'https://selenium.dunossauro.live/aula_05_b.html'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        color_scheme='dark'
    )

    page = context.new_page()
    page.goto(url)

    classes = page.locator('.linguagens')
    print(classes.text_content())

    #title = card.locator('header')
    #desc = card.locator('.description')

    #expect(title).to_have_text('teste')
    #expect(desc).to_have_text('csacsacsasacscsadsd')
    #expect(desc).to_have_text(re.compile('.*sac.*'))

    page.screenshot(path='result.png', full_page=True)
    #print(title.text_content(), ',', desc.text_content())





    sleep(1)
    browser.close()