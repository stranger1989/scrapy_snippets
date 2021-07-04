from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DetailPageSpider(CrawlSpider):
    name = "detail_page"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    rules = (
        Rule(
            LinkExtractor(restrict_xpaths=("//div[@class='quote']/span[2]/a")),
            callback="parse_item",
            follow=True,
        ),
        Rule(LinkExtractor(restrict_xpaths=("//li[@class='next']/a"))),
    )

    def parse_item(self, response):
        yield {
            "author": response.xpath("normalize-space(//h3/text())").get(),
            "born_date": response.xpath(
                "//span[@class='author-born-date']/text()"
            ).get(),
            "born_location": response.xpath(
                "//span[@class='author-born-location']/text()"
            ).get(),
            "description": response.xpath(
                "normalize-space(//div[@class='author-description']/text())"
            ).get(),
        }
