import scrapy
from scrapy.loader import ItemLoader
from scrapy_snippets.items import DownloadItem


class FileDownloadSpider(scrapy.Spider):
    name = "file_download"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        for idx, link in enumerate(response.xpath("//a[@title='Download photo']")):
            loader = ItemLoader(item=DownloadItem(), selector=link)
            relative_url = link.xpath(".//@href").extract_first()
            absolute_url = response.urljoin(relative_url)
            loader.add_value("file_urls", absolute_url)
            loader.add_xpath("file_name", f"{idx}")
            yield loader.load_item()
