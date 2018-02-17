from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
import scrapy
import re
import json


class SiteProductItem(scrapy.Item):
    Title = scrapy.Field()
    Price = scrapy.Field()
    Product_Url = scrapy.Field()


class NewEvents (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.myvaporstore.com']
    start_urls = ['http://www.myvaporstore.com/New-Ecig-Hardware-s/474.htm?searching=Y&sort=3&cat=474',
                  'http://www.myvaporstore.com/sale-hardware-s/622.htm?searching=Y&sort=3&cat=622']

    def start_requests(self):
        start_urls = self.start_urls
        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_pages)

    def parse_pages(self, response):
        page_total_count = 0
        page_links = []
        total_count = response.xpath('//font[@face="Arial"]/b/font/b/text()').extract()[1].split(' ')[2]

        if total_count:
            page_total_count = int(total_count)

        if page_total_count == 30:
            PAGE_LINK = 'http://www.myvaporstore.com/New-Ecig-Hardware-s' \
                        '/474.htm?searching=Y&sort=3&cat=474&show=20&page={page_number}'
        if page_total_count == 5:
            PAGE_LINK = 'http://www.myvaporstore.com/sale-hardware-s' \
                        '/622.htm?searching=Y&sort=3&cat=622&show=20&page={page_number}'

        for page_num in range(1, page_total_count + 1):
            link = PAGE_LINK.format(page_number=page_num)
            page_links.append(link)
        for page_link in page_links:
            yield scrapy.Request(url=page_link, callback=self._parse_product_links, dont_filter=True)

    def _parse_product_links(self, response):

        prods = response.xpath('//div[@class="v-product"]/a[@class="v-product__img"]/@href').extract()
        for prod in prods:
            yield Request(url=prod, callback=self.parse_product)

    def parse_product(self, response):
        prod_item = SiteProductItem()
        title = self._parse_title(response)
        price = self._parse_price(response)
        url = self._parse_url(response)
        prod_item['Title'] = title
        prod_item['Price'] = price
        prod_item['Product_Url'] = url
        return prod_item

    @staticmethod
    def _parse_title(response):
        title = response.xpath('//span[@itemprop="name"]//text()').extract()
        return str(title[0]) if title else " "

    @staticmethod
    def _parse_price(response):
        price = response.xpath('//span[@itemprop="price"]//text()').extract()
        return str(price[0]) if price else " "

    @staticmethod
    def _parse_url(response):
        url = response.url
        return url

