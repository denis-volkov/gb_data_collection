# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/svetodiodnye-lampy/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.parse_link)

        next_page = response.xpath("//div[@class='service-panel clearfix']//div//a["
                                   "@class='paginator-button "
                                   "next-paginator-button']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_link(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//picture[@slot]/img/@src")
        loader.add_xpath('spec', "//div[@class='def-list__group']/*/text()")
        yield loader.load_item()

        # name = response.xpath("//h1/text()").extract_first()
        # photos = response.xpath("//picture[@slot]/img/@src").extract()
        # yield LeroyparserItem(name=name, photos=photos)
