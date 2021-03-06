# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst
from datetime import datetime, timedelta

class ExtractDate(TakeFirst):
    """
    Extract date from text value.
    Possible different text patterns, 
    usually two firt words matter.
    Spider by default returns list,
    so we call TakeFirst default behaviour to extract it.
    TODO: Mabe should it be done elsewhere?
    """
    def __call__(self, values):
        string_date = super().__call__(values)
        diff_strings = self.extractDiffStrings(string_date)
        return self.parseDiff(diff_strings)

    def extractDiffStrings(self, string_date):
        """
        Extract first two words as time value and time unit.
        TODO: error detection
        """
        [time_val, time_unit] = string_date.strip().split(" ")[0:2]
        return (int(time_val), time_unit)

    def getDelta(self, diff_strings):
        (time_val, time_unit) = diff_strings
        time_unit = time_unit.lower()
        if time_unit in ["sekund", "sekundy", "sekunda", "sekundę"]:
            return timedelta(seconds = time_val)
        if time_unit in ["minut", "minuty", "minuta", "minutę"]:
            return timedelta(minutes = time_val)
        if time_unit in ["godzin", "godziny", "godzina", "godzinę"]:
            return timedelta(hours = time_val)
        if time_unit in ["dni", "dzień"]:
            return timedelta(days = time_val)
        if time_unit in ["tygodni", "tygodnie", "tydzień"]:
            return timedelta(weeks = time_val)
        if time_unit in ["miesięcy", "miesiące", "miesiąc"]:
            return timedelta(days = time_val * 30)
        if time_unit in ["lat", "lata", "rok"]:
            return timedelta(days = time_val * 365)
    
    def parseDiff(self, diff_strings):
        date_delta = self.getDelta(diff_strings)
        date = datetime.today() - date_delta
        return date.strftime('%Y-%m-%d %H:%M:%S')

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
    rating = scrapy.Field(output_processor=TakeFirst())
    comments = scrapy.Field(output_processor=TransformerComments())
    date = scrapy.Field(output_processor=ExtractDate())
