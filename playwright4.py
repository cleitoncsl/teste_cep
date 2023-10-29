from time import sleep
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(
        color_scheme='dark'
    )

    page = context.new_page()
    page.goto('http://ddg.gg')

    print(page.title())
    sleep(1)

    page.goto('https://playwright.dev/python/')
    print(page.title())
    sleep(1)

    page.go_back()
    print(page.title())
    sleep(1)
    
    page.go_forward()
    print(page.title())
    sleep(1)

    browser.close()