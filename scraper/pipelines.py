# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import traceback


class ScraperPipeline(object):
    def process_item(self, item, spider):
        return item

    # def __init__(self):
    #     self.conn = MySQLdb.connect(
    #         host='localhost',
    #         user='root',
    #         passwd='root',
    #         db='HardwareDB',
    #         charset="utf8",
    #         use_unicode=True
    #     )
    #     self.cursor = self.conn.cursor()
    #
    # def process_item(self, item, spider):
    #     try:
    #         self.cursor.execute(
    #             """INSERT INTO ScrapingTable
    #             (Name, Price, Product_Url)
    #             VALUES (%s, %s, %s)""", (
    #                 item['Name'],
    #                 item['Price'],
    #                 item['Product_Url']
    #             )
    #         )
    #
    #         self.conn.commit()
    #
    #     except MySQLdb.Error, e:
    #         print("Error %d: %s" % (e.args[0], e.args[1]))
    #
    #     return item
