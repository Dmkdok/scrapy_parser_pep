import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        peps = response.css('a.pep.reference.internal::attr(href)').getall()
        for pep in peps:
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = (
            response.css('h1.page-title::text').get().split(' – ', 1)
        )

        data = {
            'number': number,
            'name': name,
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
