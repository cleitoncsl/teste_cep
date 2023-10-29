from time import sleep
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    request = p.request.new_context()
    response = request.get('http://ddg.gg')

    print(response.status, '-', response.status_text)

