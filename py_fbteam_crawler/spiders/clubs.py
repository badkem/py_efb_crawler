from pathlib import Path

import scrapy

from py_fbteam_crawler.items import ClubItem, LeagueItem, NationalItem


class LeaguesSpider(scrapy.Spider):
    name = 'leagues'
    allowed_domains = ['efootballhub.net']

    def start_requests(self):
        url = 'https://www.efootballhub.net/efootball23/leagues'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        self.log(response.css)

        # leagues = response.selector.xpath('//div[@class="leagues-container"]')
        # self.log(f'Found {len(leagues)} leagues')
