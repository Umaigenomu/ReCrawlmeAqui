import scrapy
import re
class MisakaChan(scrapy.Spider):
    name = "MisakaChan"
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
            # "https://www.reclameaqui.com.br/"
    )

    def start_requests(self):
        for url in self.start_urls:
            if url == "https://cidadao.reclameaqui.com.br/":
                yield scrapy.Request(url, callback=self.parse_cidadao)
            else:
                yield scrapy.Request(url, callback=self.parse_regular)       

           
    def parse_cidadao(self, response):
        # Yield ONLY IF the page is eligible
        for link in response.xpath('//a/@href').extract():
            if re.search("\d+/.*", link):
                yield response.follow(link, callback=self.return_item_cidadao)
            if re.search("cidadao\.reclameaqui.*", link):
                yield response.follow(link, callback=self.parse_cidadao)

    def return_item_cidadao(self, response):
       #TODO: Check if the page is actually correct (though it should only ever get here if it is)
        yield {
            "titulo": response.xpath("//section[@class='paperblock']/p[@class='titulo']/text()").extract()[0],
            "reclamacao": "".join(response.xpath("//section[@class='paperblock']/p/text()").extract()),
            "local": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[0],
            "categoria": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[1],
            "data": response.xpath("//header[@class='header-verrec']/small/text()").extract()[0]
        }
        self.parse_cidadao(response)

    def parse_regular(self, response):
        pass
    
    def return_item_regular(self, response):
        pass

    # Sample crawl data:
# https://cidadao.reclameaqui.com.br/390323/prefeitura-rio-de-janeiro/carro-abandonado-em-via-publica-estacionado-ao-longo-de-via/
