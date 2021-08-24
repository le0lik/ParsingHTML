import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?fromSearchLine=true&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response: HtmlResponse):
        link_data = response.url
        name_data = response.xpath("//h1/text()").extract_first()
        salary_data = response.xpath("//p[@class='vacancy-salary']/span/text()").extract_first().replace(u'\u202f', '')
        yield JobparserItem(name=name_data, salary=salary_data, link=link_data, tmp=salary_data)


