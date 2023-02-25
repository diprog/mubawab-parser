from pyppeteer import launch
from pyppeteer.browser import Browser as _Browser
from pyppeteer.page import Page
import time
import urllib.parse
from lxml import etree

from . import js


async def get_attribute(page, element, attribute):
    return await page.evaluate(f'(element) => element.getAttribute("{attribute}")', element)


async def get_element_contents(page, element):
    return await page.evaluate('(element) => element.textContent', element)


async def wait_until_located_xpath(page, xpath, timeout=2):
    timeout_time = time.time() + timeout * 60
    while True:
        if time.time() >= timeout_time:
            break
        element = await page.xpath(xpath)
        if element:
            return element


class Browser:
    def __init__(self, browser: _Browser, max_pages):
        self.browser = browser
        self.max_pages = max_pages
        self.page: Page | None = None

    async def get_adv_location(self, url, location_type, location_id):
        pos = await self.page.evaluate(js.get_map_coords,
                                       url, location_type, location_id)
        return [float(p) for p in pos]

    async def get_phone_numbers_xml(self, url, adv_html) -> [str, str]:
        def get_input_value(input_id):
            input_html = adv_html.xpath(f'//input[@id="{input_id}"]')
            if input_html:
                return input_html[0].get('value')

        # Пример переменной 'function_call'
        # return showPhoneAdPage('https://www.mubawab.ma/en/ajax/desktop/web/public/show-ad-phone', 'jIb46hAZhJ2Qm4kXUASlGE8XnBGofpRrVCrQ7qVPVZ0=', 'adPage');
        phone_number_box_eh = adv_html.xpath('//div[@class="hide-phone-number-box"]')[0]
        function_call = phone_number_box_eh.get('onclick')
        _, request_url, _, encrypted_phone, _, zone_created, *_ = function_call.split("'")
        phone_numbers_html = await self.page.evaluate(
            js.get_phone_number_ajax,
            request_url,
            encrypted_phone,
            zone_created,
            'NON_PAID',
            urllib.parse.unquote(url),
            get_input_value("adIdLead"),
            get_input_value("promotionId")
        )
        return phone_numbers_html


async def create_browser(max_pages):
    options = [
        '-start-maximized',
        '--headless',
        '--disable-gpu',
        '--no-sandbox'
    ]
    browser = await launch(options={'args': options}, headless=False, ignoreDefaultArgs=True)
    pages = await browser.pages()
    await pages[0].goto('https://www.mubawab.ma/en/pa/7459743/apartment-to-purchase-in-la-gironde-5-rooms-satellite-dish-system-and-moroccan-living-room-')
    browser = Browser(browser, max_pages)
    browser.page = pages[0]
    return browser

