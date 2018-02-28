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
# CWD = os.path.dirname(os.path.abspath(__file__))
# driver_path = os.path.join(CWD, 'bin', 'chromedriver')
# driver_log_path = os.path.join(CWD, 'bin', 'driver.log')


class SiteProductItem(scrapy.Item):
    ContainerNumber = scrapy.Field()
    ContainerSizeType = scrapy.Field()
    Date = scrapy.Field()
    ContainerMoves = scrapy.Field()
    Location = scrapy.Field()
    VesselVoyage = scrapy.Field()
    VGM = scrapy.Field()


class NewEvents (scrapy.Spider):

    name = "scrapingdata"
    allowed_domains = ['www.shipmentlink.com']
    start_urls = ['https://www.shipmentlink.com/servlet/TDB1_CargoTracking.do']
    form_data = {'CNTR': 'LEAU4908755', 'TYPE': 'CNTR'}
    headers = {'Referer': 'https://www.shipmentlink.com/servlet/TDB1_CargoTracking.do',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/64.0.3282.186 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/x-www-form-urlencoded'
               }

    def start_requests(self):
        start_urls = self.start_urls
        yield Request(url=start_urls[0],
                      callback=self.parse_product,
                      headers=self.headers,
                      method='POST',
                      body=urlencode(self.form_data),
                      dont_filter=True
                      )

    def parse_product(self, response):
        prod_item = SiteProductItem()
        prod_item['ContainerNumber'] = self._parse_ContainerNumber(response)
        prod_item['ContainerSizeType'] = self._parse_ContainerSizeType(response)
        prod_item['Date'] = self._parse_Date(response)
        prod_item['ContainerMoves'] = self._parse_ContainerMoves(response)
        prod_item['Location'] = self._parse_Location(response)
        prod_item['VesselVoyage'] = self._parse_VesselVoyage(response)
        prod_item['VGM'] = self._parse_VGM(response)

        return prod_item

    @staticmethod
    def _parse_ContainerNumber(response):
        ContainerNumber = response.xpath('//table[@width="95%"][3]/tr[3]/td[1]//text()').extract()
        return str(ContainerNumber[0]) if ContainerNumber else ' '

    @staticmethod
    def _parse_ContainerSizeType(response):
        ContainerSizeType = response.xpath('//table[@width="95%"][3]/tr[3]/td[2]//text()').extract()
        return str(ContainerSizeType[0]).strip() if ContainerSizeType else ' '

    @staticmethod
    def _parse_Date(response):
        Date = response.xpath('//table[@width="95%"][3]/tr[3]/td[3]//text()').extract()
        return str(Date[0]).strip() if Date else ' '

    @staticmethod
    def _parse_ContainerMoves(response):
        ContainerMoves = response.xpath('//table[@width="95%"][3]/tr[3]/td[4]//text()').extract()
        return str(ContainerMoves[0]).strip() if ContainerMoves else ' '

    @staticmethod
    def _parse_Location(response):
        Location = response.xpath('//table[@width="95%"][3]/tr[3]/td[5]//text()').extract()
        return str(Location[0]).strip() if Location else ' '

    @staticmethod
    def _parse_VesselVoyage(response):
        VesselVoyage = response.xpath('//table[@width="95%"][3]/tr[3]/td[6]//text()').extract()
        return str(VesselVoyage[0]).strip() if VesselVoyage else ' '

    @staticmethod
    def _parse_VGM(response):
        VGM = response.xpath('//table[@width="95%"][3]/tr[3]/td[8]//text()').extract()
        return str(VGM[0]).strip() if VGM else ' '








