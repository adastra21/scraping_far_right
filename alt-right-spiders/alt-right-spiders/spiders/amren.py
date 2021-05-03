import scrapy
import json
import pandas as pd

class AmrenScraper(scrapy.Spider):
    name = "amren_spider"

    def start_requests(self):        
        start_urls = [
        "https://www.amren.com/category/news/",
        "https://www.amren.com/category/blog/",
        "https://www.amren.com/category/commentary/",
        "https://www.amren.com/category/features/"]

        for url in start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["page"] = 1
            request.meta["start_url"] = url
            yield request
    
    def parse(self, response):
        ARTICLE_XPATH = "//article/h2[contains(@class, 'title')]/a"

        for a in response.xpath(ARTICLE_XPATH):
            title = a.xpath("./text()").get()
            href = a.xpath("./@href").get()

            print("parsing %s" %title)
            yield scrapy.Request(url=response.urljoin(href),
                callback=self.parse_article, meta={"title": title})

        page = str(int(response.meta["page"]) + 1)
        start_url = response.meta["start_url"]
        new_url = start_url + "page" + "/" + page
        request = scrapy.Request(url=new_url, callback=self.parse)
        request.meta["page"] = page
        request.meta["start_url"] = start_url
        yield request

    def parse_article(self, response):
        TEXT_XPATH = "//div[contains(@class, 'the-content')]//p"
        TIME_XPATH = "//div[contains(@class, 'date')]/text()"

        title = response.meta["title"]
        url = response.url
        time = response.xpath(TIME_XPATH).get()
        time = time.strip('Posted on ')
        text = response.xpath(TEXT_XPATH).getall()

        # fix time formatting
        time = pd.to_datetime(time)
        time = time.isoformat()

        data = {"title": title,
                "text": text,
                "link": url,
                "published": time}
        
        try:
            # update filename
            with open('data/scraped_articles_amren.json', 'a') as outfile:
                json.dump(data, outfile)
        except Exception as e: print(e)