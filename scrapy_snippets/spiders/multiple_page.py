import scrapy


class MultiplePageSpider(scrapy.Spider):
    name = "multiple_page"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(".//span[1]/text()").get()
            author = quote.xpath(".//span[2]/small/text()").get()
            tags = quote.xpath(".//div/a/text()").getall()

            yield {"text": text, "author": author, "tags": tags}

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        absolute_url = f"https://quotes.toscrape.com{next_page}"
        if next_page:
            yield scrapy.Request(url=absolute_url, callback=self.parse)
