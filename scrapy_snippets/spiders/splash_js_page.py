import scrapy
from scrapy_splash import SplashRequest


class SplashJsPageSpider(scrapy.Spider):
    name = "splash_js_page"
    allowed_domains = ["quotes.toscrape.com"]

    script = """
            function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(1))
            splash:set_viewport_full()

            next_button = assert(splash:select('.next a'))
            next_button:mouse_click()
            assert(splash:wait(1))
            return splash:html()
            end
        """

    def start_requests(self):
        yield SplashRequest(
            url="https://quotes.toscrape.com/js/",
            callback=self.parse,
            endpoint="execute",
            args={"lua_source": self.script},
        )

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(".//span[1]/text()").get()
            author = quote.xpath(".//span[2]/small/text()").get()
            tags = quote.xpath(".//div/a/text()").getall()

            yield {"text": text, "author": author, "tags": tags}
