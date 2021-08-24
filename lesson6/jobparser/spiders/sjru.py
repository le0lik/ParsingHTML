import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response:HtmlResponse):
        links = response.xpath("//div[@class='f-test-search-result-item']//a[contains(@href,'vakansii')]/@href").extract()
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

        pass

    def vacancy_parse(self, response: HtmlResponse):
        link_data = response.url
        name_data = response.xpath("//h1/text()").extract_first()
        salary_data = response.xpath("//div[contains(@class,'f-test-vacancy-base-info')]/div/div/div/div/span/span").extract_first()
        yield JobparserItem(name=name_data, salary=salary_data, link=link_data, tmp=salary_data)
