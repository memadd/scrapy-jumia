# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JumiaItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    Category = scrapy.Field()
    Price = scrapy.Field()
    Description = scrapy.Field()
    Reviews = scrapy.Field()
    Rate = scrapy.Field()
    Image_link = scrapy.Field()
