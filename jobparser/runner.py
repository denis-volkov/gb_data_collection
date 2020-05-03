from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
#from jobparser import settings2
from jobparser.spiders.hhru import HhruSpider
#from jobparser.spiders.sjru import SjruSpider
if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider, text='java')
    #process.crawl(SjruSpider)
    process.start()