from time import sleep
from playwright.sync_api import sync_playwright

def event_handler(request_event):
    response = request_event.response()
    print(request_event.url)
    print(response.status)
    print(response.status, ' - ', request_event.url)


with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(
        color_scheme='dark'
    )

    page = context.new_page()

    page.on('requestfinished', event_handler)
    page.goto('http://ddg.gg')

    browser.close()