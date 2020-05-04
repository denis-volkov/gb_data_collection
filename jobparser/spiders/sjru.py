# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['russia.superjob.ru']

    def __init__(self, text):
        self.start_urls = [
            f'https://russia.superjob.ru/vacancy/search/?keywords={text}']

    def parse(self, response:HtmlResponse):
        vacancy_links = response.xpath("//a[contains(@class, '_2JivQ _1UJAN')]/@href").extract()
        for link in vacancy_links:
            yield response.follow(link, callback=self.vacancy_parse)

        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def vacancy_parse(self, response:HtmlResponse):
        name1 = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        ref1 = response.url
        salary1 = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/text()").extract()
        yield JobparserItem(name=name1, ref=ref1, salary=salary1)
