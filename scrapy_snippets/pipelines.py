# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import os
import requests

from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from scrapy.http import Request

import sqlite3
from google.cloud import bigquery
import pymongo


class ScrapySnippetsPipeline:
    def process_item(self, item, _):
        return item


class DownloaderPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        urls = ItemAdapter(item).get(self.files_urls_field, [])
        return [Request(u, meta={"filename": item.get("file_name")}) for u in urls]

    def file_path(self, request, response=None, info=None, *, item=None):
        media_ext = os.path.splitext(request.url)[1]
        return f"download/{request.meta['filename']}{media_ext}"


class SlackPipeline:
    def close_spider(self, _):
        # send screenshot to slack
        files = {"file": open("screenshot.png", "rb")}
        param = {"token": os.environ["SLACK_TOKEN"], "channels": os.environ["CHANNELS"]}
        requests.post("https://slack.com/api/files.upload", params=param, files=files)


class SQLlitePipeline(object):
    def open_spider(self, _):
        self.connection = sqlite3.connect("to_scrape.db")
        self.c = self.connection.cursor()
        self.c.execute(
            """
            CREATE TABLE to_scrape(
                text TEXT,
                author TEXT,
                tags TEXT
            )
        """
        )
        self.connection.commit()

    def close_spider(self, _):
        self.connection.close()

    def process_item(self, item, _):
        self.c.execute(
            """
            INSERT INTO to_scrape (text,author,tags) VALUES(?,?,?)
        """,
            (
                item.get("text"),
                item.get("author"),
                ",".join(map(str, item.get("tags"))),
            ),
        )
        self.connection.commit()
        return item


class BigqueryPipeline:
    def open_spider(self, _):
        self.client = bigquery.Client()
        self.items = []

    def close_spider(self, spider):
        errors = self.client.insert_rows_json(
            os.environ["BIGQUERY_TABLE_NAME"], self.items
        )
        if errors == []:
            print("New rows have been added.")
        else:
            spider.crawler.engine.close_spider(self, reason=errors)
        self.client.close()

    def process_item(self, item, _):
        self.items.append(
            {
                "text": item.get("text"),
                "author": item.get("author"),
                "tags": item.get("tags"),
            }
        )
        return item


class MongodbPipeline:
    def open_spider(self, _):
        self.client = pymongo.MongoClient(os.environ["MONGO_CONNECTION_STRING"])
        self.db = self.client[os.environ["MONGO_DATABASE_NAME"]]

    def close_spider(self, _):
        self.client.close()

    def process_item(self, item, _):
        self.db[os.environ["MONGO_COLLECTION_NAME"]].insert(item)
        return item
