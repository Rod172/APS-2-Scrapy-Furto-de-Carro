import scrapy 
from read import red_csv, read_excel

base_url = 'url do site'

class SoSpider(scrapy.Spider):
    name = 'so'
    
    def start_requests(self):
        for tag in read_excel():
            yield scrapy.Request(base_url.format(tag))
    
    def parse(self, response):
        questions = response.xpath('normalize-space(//*[@id="mainbar"]/div[4]/div/div[1]/text())').get()
        questions = questions.strip('questions')

        yield {
            'questions': questions,
            'url': response.url
        }