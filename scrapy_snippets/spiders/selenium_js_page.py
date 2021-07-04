import scrapy

from scrapy.selector import Selector
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumJsPageSpider(scrapy.Spider):
    name = "selenium_js_page"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js/"]

    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")

        # driver = webdriver.Remote(command_executor="http://localhost:4444")
        driver = webdriver.Chrome(
            executable_path="./chromedriver", options=chrome_options
        )
        driver.get("https://quotes.toscrape.com/js/")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
        driver.find_element_by_xpath('//li[@class="next"]/a').click()
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located)
        driver.find_element_by_xpath('//li[@class="next"]/a').click()
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp = Selector(text=self.html)
        quotes = resp.xpath("//div[@class='quote']")
        for quote in quotes:
            text = quote.xpath(".//span[1]/text()").get()
            author = quote.xpath(".//span[2]/small/text()").get()
            tags = quote.xpath(".//div/a/text()").getall()

            yield {"text": text, "author": author, "tags": tags}
