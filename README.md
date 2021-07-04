# Scrapy Snippets

Scrapy spider snippets for web crawling and web scraping.<br />
You can also scrape web page controlled by javascript using selenium or splash.

## Requirements
- Python 3.9+

## Install required packages
Install pipenv in global at first.

```shell
pip install pipenv
```

Install required packages via pipenv afterwards. <br />
** Refer `./Pipfile` regarding details for packages.

```
pipenv install
# or
pipenv install --dev
```

If you'd like to make virtual env on project root, set ENV as below.

```
# for mac or linux
export PIPENV_VENV_IN_PROJECT=true
# for win
set PIPENV_VENV_IN_PROJECT=true
```

## Available scrapy tool commands

You can see all available commands with.
```
pipenv run scrapy -h
```

### Some example

- Start crawling using a spider.

```
pipenv run scrapy crawl <spider_name>
```

- Generate new spider using pre-defined templates.

```
pipenv run scrapy genspider <mydomain> <mydomain_url.com>
```

## Initial spider list

|  file name  |  spider name  |  description  |
| :--- | :--- | :--- |
|  single_page.py  |  single_page  |  scraping basic example   |
|  multiple_page.py  |  multiple_page  |  scrape multiple pages example |
|  detail_page.py  |  detail_page  |  crawling example  |
|  splash_js_page.py  |  splash_js_page  |  splash example  |
|  selenium_js_page.py  |  selenium_js_page  |  selenium example  |
|  scrapy_selenium_js_page.py  |  scrapy-selenium_js_page  |  selenium example using scrapy package |
|  login_page.py  |  login_page  | scrape login page basic |
|  selenium_js_login_page.py  |  selenium_js_login_page  | selenium login |
| file_download.py | file_download | file download example * image download from unsplash |
| selenium_screenshot.py | selenium_screenshot | take a screenshot by selenium example |

## Export to file using command line

|  file format  |  command line  |
| :--- | :--- |
|  csv  |  pipenv run scrapy crawl <spider_name> -o <output_filename>.csv |
|  json  |  pipenv run scrapy crawl <spider_name> -o <output_filename>.json  |
|  xml  |  pipenv run scrapy crawl <spider_name> -o <output_filename>.xml  |

## Export to database via pipeline

Enable the pipeline by adding it to `ITEM_PIPELINES` in the `settings.py` file and changing some pipeline name active.<br />
** It just display the result in your console if use as default.

```
ITEM_PIPELINES = {
    "scrapy_snippets.pipelines.ScrapySnippetsPipeline": 0,
    # "scrapy_snippets.pipelines.DownloaderPipeline": 1,
    # "scrapy_snippets.pipelines.SQLlitePipeline": 2,
    # "scrapy_snippets.pipelines.BigqueryPipeline": 3,
    # "scrapy_snippets.pipelines.MongodbPipeline": 4,
    # "scrapy_snippets.pipelines.SlackPipeline": 5
}
```


|  DB  |  pipeline name  |
| :--- | :--- |
|  SQLite  | SQLlitePipeline |
|  Bigquery  |  BigqueryPipeline  |
|  MongoDB  | MongodbPipeline |

## File download via pipeline

|  format  |  pipeline name  |
| :--- | :--- |
|  jpg, xls, mp3 ..etc  | DownloaderPipeline |

## Send to other services via pipeline

|  Service  |  pipeline name  |
| :--- | :--- |
|  Slack  | SlackPipeline |

## Selenium

To execute selenium, require web driver chrome or firefox and so on.., so you should download it from following url.<br />
Next, place driver on this project root.

> https://www.selenium.dev/documentation/en/webdriver/driver_requirements/

## Splash
Install Docker. Make sure Docker version >= 17 is installed.<br />
Pull and start container as below command.

```
docker-compose up -d
```
Splash is now available at 0.0.0.0 at port 8050
