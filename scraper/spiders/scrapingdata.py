from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
import scrapy
import re
import json
import os
import time
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
    allowed_domains = ['www.shipmentlink.com']
    start_urls = ['https://www.shipmentlink.com/servlet/TDB1_CargoTracking.do']

    def start_requests(self):
        start_urls = self.start_urls
        yield scrapy.Request(url=start_urls[0], callback=self.parse_pages)

    def parse_pages(self, response):
        page_links = []

        if response.url == 'https://www.vapordna.com/Devices-s/1814.htm':
            page_links = ['https://www.vapordna.com/Devices-s/1814.htm']

        for page_link in page_links:
            yield scrapy.Request(url=page_link, callback=self._parse_product_links, dont_filter=True)

    def _parse_product_links(self, response):

        if response.xpath('//div[@class="product__image"]/a/@href').extract():
            prods = response.xpath('//div[@class="product__image"]/a/@href').extract()
            for prod in prods:
                yield Request(url='https://www.electrictobacconist.com' + prod, callback=self.parse_product)

    def parse_product(self, response):
        prod_item = SiteProductItem()
        name = self._parse_name(response)
        price = self._parse_price(response)
        url = self._parse_url(response)
        prod_item['Name'] = name
        prod_item['Price'] = price
        prod_item['Product_Url'] = url
        return prod_item

    @staticmethod
    def _parse_name(response):
        if response.xpath('//span[@itemprop="name"]//text()').extract():
            name = response.xpath('//span[@itemprop="name"]//text()').extract()[0]

        return str(name) if name else " "

    @staticmethod
    def _parse_price(response):
        if response.xpath('//span[@itemprop="price"]//text()').extract():
            price = response.xpath('//span[@itemprop="price"]//text()').extract()

        return str(price[0]) if price else " "

    @staticmethod
    def _parse_url(response):
        url = response.url
        return url






