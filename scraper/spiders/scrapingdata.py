from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
import scrapy
import re
import json
import csv
import os
import time
import requests

# from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# CWD = os.path.dirname(os.path.abspath(__file__))
# driver_path = os.path.join(CWD, 'bin', 'chromedriver')
# driver_log_path = os.path.join(CWD, 'bin', 'driver.log')

# keys = ['LEAU4908550', 'LEAU4908565', 'LEAU4908605', 'LEAU4908610', 'LEAU4908734', 'LEAU4908755']
keys = ['SESU2195470', 'SESU2195253', 'SESU2195232', 'SESU2195227']
# keys = []
# try:
#     with open(os.path.abspath('inputdata.csv'), 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             keys.append(row[0])
# except Exception as e:
#     print('parse_csv Function => Got Error: {}'.format(e))
#
#     with open('/home/ubuntu/Marin-Guru/container_scraping/ScrapingContainer-MySQL/inputdata/inputdata.csv', 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             keys.append(row[0])


class SiteProductItem(scrapy.Item):
    container_num = scrapy.Field()
    container_sizetype = scrapy.Field()
    date = scrapy.Field()
    container_moves = scrapy.Field()
    location = scrapy.Field()
    vessel_voyage = scrapy.Field()
    vgm = scrapy.Field()
    weight = scrapy.Field()
    origin = scrapy.Field()
    landing_port = scrapy.Field()
    TS_port = scrapy.Field()
    discharging_port = scrapy.Field()
    destination = scrapy.Field()
    ServiceTerm = scrapy.Field()


class NewEvents (scrapy.Spider):

    name = "scrapingdata"
    allowed_domains = ['www.shipmentlink.com', 'www.hmm.co.kr']

    start_urls = ['https://www.shipmentlink.com/servlet/TDB1_CargoTracking.do',
                  'http://www.hmm.co.kr/ebiz/track_trace/trackCTPv8.jsp?'
                  'blFields=undefined&cnFields=undefined&numbers=&numbers='
                  '&numbers=&numbers=&numbers=&numbers=&numbers=&numbers='
                  '&numbers=&numbers={}&numbers=&numbers=&numbers=&numbers='
                  '&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers='
                  ]
    # start_urls = ['http://www.hmm.co.kr/ebiz/track_trace/trackCTPv8.jsp?'
    #               'blFields=undefined&cnFields=undefined&numbers=&numbers='
    #               '&numbers=&numbers=&numbers=&numbers=&numbers=&numbers='
    #               '&numbers=&numbers={}&numbers=&numbers=&numbers=&numbers='
    #               '&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=&numbers=']

    # start_urls = ['https://www.shipmentlink.com/servlet/TDB1_CargoTracking.do']

    def start_requests(self):
        for start_url in self.start_urls:
            for key in keys:
                if 'www.shipmentlink.com' in start_url:
                    form_data = {'CNTR': key, 'TYPE': 'CNTR', 'blFields': '1', 'cnFields': '1', 'is-quick': 'Y'}
                    yield Request(url=start_url,
                                  headers={
                                            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                            'Chrome/64.0.3282.186 Safari/537.36',
                                            'Content-Type': 'application/x-www-form-urlencoded'
                                           },
                                  callback=self.parse_product,
                                  method='POST',
                                  body=urlencode(form_data),
                                  dont_filter=True)

                if 'www.hmm.co.kr' in start_url:
                    form_data = {'number': 'SESU2195470', 'numbers': 'SESU2195470'}
                    yield Request(url=start_url.format(key),
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                                    ' Chrome/64.0.3282.186 Safari/537.36',
                                      'Content-Type': 'application/x-www-form-urlencoded',
                                      'Referer': 'http://www.hmm.co.kr/ebiz/track_trace/main_new.jsp?type=2&number=SESU2195470'
                                                 '&is_quick=Y&quick_params='
                                  },
                                  method='POST',
                                  callback=self.parse_product,
                                  body=urlencode(form_data),
                                  dont_filter=True)

    def parse_product(self, response):

        prod_item = SiteProductItem()

        prod_item['container_num'] = self._parse_ContainerNumber(response)
        prod_item['container_sizetype'] = self._parse_ContainerSizeType(response)
        prod_item['date'] = self._parse_Date(response)
        prod_item['container_moves'] = self._parse_ContainerMoves(response)
        prod_item['location'] = self._parse_Location(response)
        prod_item['vessel_voyage'] = self._parse_VesselVoyage(response)
        prod_item['vgm'] = self._parse_VGM(response)
        prod_item['weight'] = self._parse_weight(response)
        prod_item['origin'] = self._parse_origin(response)
        prod_item['landing_port'] = self._parse_landing_port(response)
        prod_item['TS_port'] = self._parse_TS_port(response)
        prod_item['discharging_port'] = self._parse_discharging_port(response)
        prod_item['destination'] = self._parse_destination(response)
        prod_item['ServiceTerm'] = self._parse_ServiceTerm(response)

        return prod_item

    @staticmethod
    def _parse_ContainerNumber(response):
        try:
            ContainerNumber = response.xpath('//table[@width="95%"][3]/tr[3]/td[1]//text()').extract()
            if ContainerNumber:
                ContainerNumber = str(ContainerNumber[0])
            if not ContainerNumber:
                ContainerNumber = str(response.xpath('//td[@class="bor_L_none"]/a/font/u//text()')[0].extract())
            return ContainerNumber if ContainerNumber else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_ContainerSizeType(response):
        try:
            ContainerSizeType = response.xpath('//table[@width="95%"][3]/tr[3]/td[2]//text()').extract()
            if ContainerSizeType:
                ContainerSizeType = str(ContainerSizeType[0]).strip()
            if not ContainerSizeType:
                ContainerSizeType = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[18])
            return ContainerSizeType if ContainerSizeType else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_Date(response):
        try:
            Date = response.xpath('//table[@width="95%"][3]/tr[3]/td[3]//text()').extract()
            if Date:
                Date = str(Date[0]).strip()
            if not Date:
                Date = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[53])
            return Date if Date else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_ContainerMoves(response):
        try:
            ContainerMoves = response.xpath('//table[@width="95%"][3]/tr[3]/td[4]//text()').extract()
            if ContainerMoves:
                ContainerMoves = str(ContainerMoves[0]).strip()
            if not ContainerMoves:
                ContainerMoves = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[22])
            return ContainerMoves if ContainerMoves else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_Location(response):
        try:
            Location = response.xpath('//table[@width="95%"][3]/tr[3]/td[5]//text()').extract()
            if Location:
                Location = str(Location[0]).strip()
            if not Location:
                Location = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[21])
            return Location if Location else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_VesselVoyage(response):
        try:
            VesselVoyage = response.xpath('//table[@width="95%"][3]/tr[3]/td[6]//text()').extract()
            if VesselVoyage:
                VesselVoyage = str(VesselVoyage[0]).strip()
            if not VesselVoyage:
                VesselVoyage = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[57])
            return VesselVoyage if VesselVoyage else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_VGM(response):
        try:
            VGM = response.xpath('//table[@width="95%"][3]/tr[3]/td[8]//text()').extract()
            return str(VGM[0]).strip() if VGM else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_weight(response):
        try:
            weight = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[19])
            return weight if weight else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_origin(response):
        try:
            origin = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[1])
            return origin if origin else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_landing_port(response):
        try:
            landing_port = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[2])
            return landing_port if landing_port else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_TS_port(response):
        try:
            ts_port = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[3])
            return ts_port if ts_port else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_discharging_port(response):
        try:
            charging_port = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[4])
            return charging_port if charging_port else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_destination(response):
        try:
            destination = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[5])
            return destination if destination else ' '
        except Exception as e:
            print('Error')

    @staticmethod
    def _parse_ServiceTerm(response):
        try:
            ServiceTerm = str(response.xpath('//div[@class="base_table01"]/table/tbody/tr/td/text()').extract()[20])
            return ServiceTerm.strip() if ServiceTerm else ' '
        except Exception as e:
            print('Error')









