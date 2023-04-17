# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PyFbteamCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LeagueItem(scrapy.Item):
    name = scrapy.Field()
    logo = scrapy.Field()


class NationalItem(scrapy.Item):
    countryName = scrapy.Field()
    flag = scrapy.Field()


class ClubItem(scrapy.Item):
    name = scrapy.Field()
    logo = scrapy.Field()
    league = scrapy.Field()
