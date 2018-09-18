from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy

class ReCrawler(CrawlSpider):
    name = "ReCrawler"
    allowed_domains = ['cidadao.reclameaqui.com.br', 'reclameaqui.com.br']
    # custom_settings = {
    #     'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    #     'AUTO_THROTTLE_ENABLED': True,
    #     'COOKIES_ENABLED': False,
    #     'ITEM_PIPELINES': {
    #         'ReCrawlmeAqui.pipelines.RecrawlmeaquiPipeline': 300
    #     }
    # }

    start_urls = (
            "https://cidadao.reclameaqui.com.br/",
            "https://www.reclameaqui.com.br/"
    )
    rules = (
        # Cidadao
        Rule(LinkExtractor(allow=(r"cidadao\.reclameaqui.*",)), follow=True),
        Rule(LinkExtractor(allow=(r"\d+/.*",)), callback='parse_cidadao', follow=True),
        # Regular
        # Rule(LinkExtractor(allow=r"www\.reclameaqui"), callback=lambda r: print(r.url), follow=True),
        # Rule(LinkExtractor(allow="cidadao\.reclameaqui\.com\.br/\d+/.*"), callback='parseRegular', follow=True),
    )


    def parse_cidadao(self, response):
        # Yield ONLY IF the page is eligible
        # if ...
        return scrapy.Item({
            "titulo": response.xpath("//p[@class='titulo']/text()").extract()[0],
            "reclamacao": "".join(response.xpath("//section[@class='paperblock']/p/text()").extract()),
            "local": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[0],
            "categoria": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[1],
            "time": response.xpath("//header[@class='header-verrec']/small/text()").extract()[0]
        })

    def parseRegular(self, response):
        pass
# Sample crawl data:
# https://cidadao.reclameaqui.com.br/390323/prefeitura-rio-de-janeiro/carro-abandonado-em-via-publica-estacionado-ao-longo-de-via/
