from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
import scrapy
import re
import json
import os
import time
# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

CWD = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(CWD, 'bin', 'chromedriver')
driver_log_path = os.path.join(CWD, 'bin', 'driver.log')


class SiteProductItem(scrapy.Item):
    # ContainerNumber = scrapy.Field()
    # ContainerSizeType = scrapy.Field()
    # ShippingLine = scrapy.Field()
    # LatestEvent = scrapy.Field()
    Origin = scrapy.Field()
    # FinalDestination = scrapy.Field()
    # ETA = scrapy.Field()
    # PortofDischarge = scrapy.Field()
    # Destination = scrapy.Field()
    # EmptyReturnLocation = scrapy.Field()


class NewEvents (scrapy.Spider):

    name = "scrapingdata"
    allowed_domains = ['www.oocl.com']
    start_urls = ['http://www.oocl.com/eng/Pages/default.aspx']

    def start_requests(self):
        start_urls = self.start_urls
        # for start_url in start_urls:
        #     yield scrapy.Request(url=start_url, callback=self.parse_pages)
        yield scrapy.Request(url=start_urls[0], callback=self.parse_pages)

    def parse_pages(self, response):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        browser = webdriver.Chrome(
            executable_path=driver_path,
            service_log_path=driver_log_path,
            chrome_options=options
        )

        # browser.set_window_size(1440, 900)
        browser.maximize_window()
        browser.implicitly_wait(100)
        browser.set_page_load_timeout(100)
        browser.get(response.url)
        # if browser.find_element_by_xpath('//ul[contains(@class, "dropdown-menu")]'):
        #     search_type = browser.find_element_by_xpath('//ul[contains(@class, "dropdown-menu")]'
        #                                                 '/li[3]/a')
        # if not search_type:
        search_type = browser.find_element_by_xpath('//select[@id="ooclCargoSelector"]/option[@value="cont"]')
        if search_type:
            search_type.click()

        search_input = browser.find_element_by_id("SEARCH_NUMBER")
        search_input.send_keys('LEAU4908966')
        search_button = browser.find_element_by_id('container_btn')
        search_button.click()

        page_content = browser.page_source

        product = SiteProductItem()
        product['Origin'] = page_content

        return product

