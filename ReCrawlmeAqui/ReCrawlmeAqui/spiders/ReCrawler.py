from scrapy.spiders import CrawlSpider, Rule
import scrapy

class ReCrawler(CrawlSpider):
    name = "ReCrawler"
    # custom_settings = {
    #     'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
    #     'AUTO_THROTTLE_ENABLED': True,
    #     'COOKIES_ENABLED': False,
    #     'ITEM_PIPELINES': {
    #         'ReCrawlmeAqui.pipelines.RecrawlmeaquiPipeline': 300
    #     }
    # }

    def start_requests(self):
        start_urls = [
            "https://cidadao.reclameaqui.com.br/",
            "https://www.reclameaqui.com.br/"
        ]
        for url in start_urls:
            if url == "https://cidadao.reclameaqui.com.br/":
                yield scrapy.Request(url, self.parseCidadao)
            else:
                yield scrapy.Request(url. self.parseRegular)

    def parseCidadao(self, response):
        # Yield ONLY IF the page is eligible
        # if ...
        yield {
            "titulo": response.xpath("//p[@class='titulo']/text()").extract()[0],
            "reclamacao": "".join(response.xpath("//section[@class='paperblock']/p/text()").extract()),
            "local": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[0],
            "categoria": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[1]
        }


    def parseRegular(self, response):
        pass
# Sample crawl data:
# https://cidadao.reclameaqui.com.br/390323/prefeitura-rio-de-janeiro/carro-abandonado-em-via-publica-estacionado-ao-longo-de-via/
