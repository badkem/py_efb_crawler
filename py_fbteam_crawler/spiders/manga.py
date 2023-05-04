from scrapy import Spider, Selector, Request

from py_fbteam_crawler.items import MangaItem, MangaChapterItem

import json


class MangaSpider(Spider):
    with open('secret_domains.json') as f:
        dm = json.load(f)
        url_name = dm['hehe']['url_name']
        base_url = dm['hehe']['url']
        print(f'no one cant know me {url_name}')

    name = 'manga'
    allowed_domains = [url_name]

    post = MangaItem()
    post_item = MangaChapterItem()

    def start_requests(self):
        url = self.base_url
        self.f.close()
        yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        manga_list = Selector(response).xpath('//div[@class="col post-item"]')
        self.log(f'Manga found: {len(manga_list)}')
        for manga in manga_list:
            self.post['url'] = manga.xpath('./div[@class="col-inner"]/a/@href').get()
            self.post['title'] = manga.xpath('.//h5[@class="post-title is-small uppercase"]/text()').get()
            self.post['date'] = manga.xpath('.//div[@class="post-meta "]/text()').extract()[0]
            self.post['viewers'] = manga.xpath('.//div[@class="post-meta "]/text()').extract()[1]
            self.post['image_url'] = manga.css('img::attr(data-lazy-src)').get()

            yield Request(self.post['url'], callback=self.parse_chapter_detail)

    def parse_chapter_detail(self, response):
        chapter_list = Selector(response).xpath('//div[@class="list_issues"]/div')
        for chap in chapter_list:
            title = chap.xpath('.//div[@class="col large-8 small-4"]/a/text()').get()

            self.post_item['title'] = title.strip() if title else None
            self.post_item['url'] = chap.xpath('./div[@class="col large-8 small-4"]/a/@href').get()
            self.post_item['chap_viewers'] = chap.xpath('./div[@class="col large-2 small-4 text-center"]/text()').get()
            self.post_item['chap_date'] = chap.xpath('./div[@class="col large-2 small-3 text-center"]/text()').get()
            self.post_item['chap_images'] = []

            if self.post_item['url']:
                yield Request(self.post_item['url'], callback=self.get_chapter_images)

    def get_chapter_images(self, response):
        list_image = Selector(response).xpath('//div[@class="list-images"]/img')
        for image in list_image:
            self.post_item['chap_images'].append(image.css("img::attr(data-lazy-src)").get())

        self.post['chapters'] = []
        self.post['chapters'].append(dict(self.post_item))

        yield self.post
