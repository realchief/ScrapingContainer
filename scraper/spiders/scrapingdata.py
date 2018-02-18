from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
import scrapy
import re
import json


class SiteProductItem(scrapy.Item):
    Name = scrapy.Field()
    Price = scrapy.Field()
    Product_Url = scrapy.Field()


class NewEvents (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.myvaporstore.com', 'www.vapordna.com', 'vaping.com',
                       'www.directvapor.com', 'www.vapestore.co.uk', 'www.migvapor.com',
                       'www.electrictobacconist.com']
    start_urls = ['http://www.myvaporstore.com/New-Ecig-Hardware-s/474.htm?searching=Y&sort=3&cat=474',
                  'https://www.vapordna.com/Devices-s/1814.htm',
                  'https://vaping.com/vape-mods',
                  'https://www.vapestore.co.uk/black-friday/hardware/',
                  'https://www.migvapor.com/electronic-cigarettes/advanced-e-cigarette-kits',
                  'https://www.electrictobacconist.com/e-cigarette-kits-c1']
    # start_urls = ['https://www.vaporfi.com/electronic-cigarettes/?limit=all']

    def start_requests(self):
        start_urls = self.start_urls
        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse_pages)

    def parse_pages(self, response):
        page_total_count = 0
        page_links = []
        if response.url == 'http://www.myvaporstore.com/New-Ecig-Hardware-s/474.htm?searching=Y&sort=3&cat=474':
            total_count = response.xpath('//font[@face="Arial"]/b/font/b/text()').extract()[1].split(' ')[2]

            if total_count:
                page_total_count = int(total_count)

            if page_total_count == 30:
                PAGE_LINK = 'http://www.myvaporstore.com/New-Ecig-Hardware-s' \
                            '/474.htm?searching=Y&sort=3&cat=474&show=20&page={page_number}'

            for page_num in range(1, page_total_count + 1):
                link = PAGE_LINK.format(page_number=page_num)
                page_links.append(link)

        if response.url == 'https://www.vapordna.com/Devices-s/1814.htm':
            page_links = ['https://www.vapordna.com/Devices-s/1814.htm']

        if response.url == 'https://vaping.com/vape-mods':
            page_links = ['https://vaping.com/vape-mods']

        if response.url == 'https://www.vapestore.co.uk/black-friday/hardware/':
            page_links = ['https://www.vapestore.co.uk/black-friday/hardware/']

        if response.url == 'https://www.migvapor.com/electronic-cigarettes/advanced-e-cigarette-kits':
            page_links = ['https://www.migvapor.com/electronic-cigarettes/advanced-e-cigarette-kits']

        if response.url == 'https://www.electrictobacconist.com/e-cigarette-kits-c1':
            page_links = ['https://www.electrictobacconist.com/e-cigarette-kits-c1']

        for page_link in page_links:
            yield scrapy.Request(url=page_link, callback=self._parse_product_links, dont_filter=True)

    def _parse_product_links(self, response):

        if response.xpath('//div[@class="product__image"]/a/@href').extract():
            prods = response.xpath('//div[@class="product__image"]/a/@href').extract()
            for prod in prods:
                yield Request(url='https://www.electrictobacconist.com' + prod, callback=self.parse_product)

        if response.xpath('//div[@class="v-product"]/a[@class="v-product__img"]/@href').extract():
            prods = response.xpath('//div[@class="v-product"]/a[@class="v-product__img"]/@href').extract()
            for prod in prods:
                yield Request(url=prod, callback=self.parse_product)

        if response.xpath('//div[contains(@class, "promo")]/a/@href').extract():
            prods = response.xpath('//div[contains(@class, "promo")]/a/@href').extract()
            for prod in prods:
                yield Request(url=prod, callback=self.parse_product)

        if response.xpath('//li[@class="item"]/a[@class="product-image"]/@href').extract():
            prods = response.xpath('//li[@class="item"]/a[@class="product-image"]/@href').extract()
            for prod in prods:
                yield Request(url=prod, callback=self.parse_product)

        if response.xpath('//li[@class="item isotope-item"]/a[@class="item-content"]/@href').extract():
            prods = response.xpath('//li[@class="item isotope-item"]/a[@class="item-content"]/@href').extract()
            for prod in prods:
                yield Request(url=prod, callback=self.parse_product)

        if response.xpath('//div[@class="product-image-area"]/a/@href').extract():
            prods = response.xpath('//div[@class="product-image-area"]/a/@href').extract()
            for prod in prods:
                yield Request(url=prod, callback=self.parse_product)

        if response.xpath('//div[@class="product--image-link"]/@href').extract():
            prods = response.xpath('//div[@class="product--image-link"]/@href').extract()
            for prod in prods:
                yield Request(url='https://www.vapestore.co.uk' + prod, callback=self.parse_product)

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

        if response.xpath('//div[@class="name"]/text()').extract():
            name = response.xpath('//div[@class="product-name"]//div[@class="name"]/text()').extract()[0].strip()

        if response.xpath('//h1[@class="listing--title"]/text()').extract():
            name = response.xpath('//h1[@class="listing--title"]/text()').extract()[0].strip()

        if response.xpath('//h1[@itemprop="name"]/text()').extract():
            name = response.xpath('//h1[@itemprop="name"]/text()').extract()[0].strip()

        if response.xpath('//span[@class="product-content__title--brand"]/text()').extract():
            name = response.xpath('//span[@class="product-content__title--brand"]/text()').extract()[0].strip()

        if response.xpath('//div[@class="product-name"]/h1/text()').extract():
            name = response.xpath('//div[@class="product-name"]/h1/text()').extract()[0].strip()

        return str(name) if name else " "

    @staticmethod
    def _parse_price(response):
        if response.xpath('//span[@itemprop="price"]//text()').extract():
            price = response.xpath('//span[@itemprop="price"]//text()').extract()

        if response.xpath('//span[@class="price"]//text()').extract():
            price = response.xpath('//span[@class="price"]//text()').extract()[0].strip()

        if response.xpath('//span[@class="USD"]//text()').extract():
            price = response.xpath('//span[@class="USD"]//text()').extract()

        return str(price[0]) if price else " "

    @staticmethod
    def _parse_url(response):
        url = response.url
        return url

