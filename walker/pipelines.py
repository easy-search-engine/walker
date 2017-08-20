# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
EXPORT_URL = "http://localhost/search-engine/public/item"

class ExportPipeline(object):
    def process_item(self, item, spider):
        response = requests.post(EXPORT_URL, {
            "src": item['src'],
            "date": item['date'],
            "rating": item['rating']
        })
        return item
