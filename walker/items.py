# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst

class TransformerComments(TakeFirst):
    def __call__(self, values):
        string_comments = super().__call__(values)
        string_comments = string_comments.replace("\n","")
        string_comments = string_comments.replace(" ","")
        return string_comments

class Meme(scrapy.Item):
    """
    Basic meme model
    """
    src = scrapy.Field(output_processor=TakeFirst())
    tags = scrapy.Field()
    comments = scrapy.Field(output_processor=TransformerComments())