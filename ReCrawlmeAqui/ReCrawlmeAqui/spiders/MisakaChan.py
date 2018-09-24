import scrapy
import re


class MisakaChan(scrapy.Spider):
    name = "MisakaChan"
    allowed_domains = ['cidadao.reclameaqui.com.br']
    base_cidadao = "https://cidadao.reclameaqui.com.br/"
    start_urls = (
        "https://cidadao.reclameaqui.com.br/listareclamacoes/?screen=0&show=1&id=&qr=&categoria=&servico=&tipo=",
    )

    def __init__(self, name="MisakaChan", **kwargs):
        super(MisakaChan, self).__init__(name, kwargs)
        self.next_page = 1
        self.cidadao_template = "https://cidadao.reclameaqui.com.br/listareclamacoes/\
        ?screen={}&show=1&id=&qr=&categoria=&servico=&tipo="

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_cidadao)

    def parse_cidadao(self, response):
        for link in response.xpath('//@href').extract():
            if re.search(r"\d+/", link) and not (
                    re.match(r"^javascript.*$", link) or
                    re.search(r"listareclamacoes", link) or
                    re.search(r"js", link)):
                yield scrapy.Request(self.base_cidadao + link, callback=self.return_item_cidadao)

        if self.next_page <= 7230:
            yield scrapy.Request(self.cidadao_template.format(self.next_page), callback=self.parse_cidadao)
            self.next_page += 1

    def return_item_cidadao(self, response):
        # The page should only ever get here if it is eligible for extracting the elements below
        yield {
            "titulo": response.xpath("//section[@class='paperblock']/p[@class='titulo']/text()").extract()[0],
            "reclamacao": "".join(response.xpath("//section[@class='paperblock']/p/text()").extract()),
            "local": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[0],
            "categoria": response.xpath("//ul[@id='details']/li/p/a/text()").extract()[1],
            "data": response.xpath("//header[@class='header-verrec']/small/text()").extract()[0]
        }
        # self.parse_cidadao(response)

# Sample scrape data:
# https://cidadao.reclameaqui.com.br/390323/prefeitura-rio-de-janeiro/carro-abandonado-em-via-publica-estacionado-ao-longo-de-via/
