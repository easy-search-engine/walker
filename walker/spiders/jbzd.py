# -*- coding: utf-8 -*-
import scrapy
from walker.items import Meme
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider


class JbzdSpider(Spider):
    name = 'jbzd'
    allowed_domains = [
        'jbzd.pl',
        'jbzdy.pl'
    ]
    start_urls = ['http://jbzd.pl/']


    def parse(self, response):
        for memeContainer in response.xpath("//div[@class='content-info' and not(descendant::video)]"):
            loader = ItemLoader(Meme(),memeContainer)
            loader.add_xpath('src', ".//div[@class='media']/descendant::img/@src")
            loader.add_xpath('tags', ".//div[@class='info']/div[@class='tags']/a[@class='tag']/@data-tag")
            loader.add_xpath('date', ".//div[@class='info']/span[1]/text()")
            yield loader.load_item()

        next_link = response.xpath("//a[@class='btn-next-page']/@href").extract_first()
        next_link = response.urljoin(next_link)
        yield scrapy.Request(
            url = next_link,
            callback = self.parse
        )