import scrapy
from scrapy_selenium import SeleniumRequest


class ScrapySeleniumJsPageSpider(scrapy.Spider):
    name = "scrapy-selenium_js_page"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://quotes.toscrape.com/js/", wait_time=3, callback=self.parse
        )

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(".//span[1]/text()").get()
            author = quote.xpath(".//span[2]/small/text()").get()
            tags = quote.xpath(".//div/a/text()").getall()

            yield {"text": text, "author": author, "tags": tags}
