import scrapy
import json
import pandas as pd

class BreitbartSpider(scrapy.Spider):
    name = "breitbart_spider"

    def start_requests(self):        
        start_urls = [
        "https://www.breitbart.com/politics/",
        "https://www.breitbart.com/entertainment/",
        "https://www.breitbart.com/the-media/",
        "https://www.breitbart.com/economy/",
        "https://www.breitbart.com/europe/",
        "https://www.breitbart.com/border/",
        "https://www.breitbart.com/middle-east/",
        "https://www.breitbart.com/africa/",
        "https://www.breitbart.com/asia/",
        "https://www.breitbart.com/latin-america/",
        "https://www.breitbart.com/world-news/",
        "https://www.breitbart.com/tech/",
        "https://www.breitbart.com/sports/",
        "https://www.breitbart.com/tag/on-the-hill/",
        # "https://www.breitbart.com/news/source/breitbart-news/",
        "https://www.breitbart.com/tag/b-inspired-news/",
        ]
        for url in start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["page"] = 1
            request.meta["start_url"] = url
            yield request
    
    def parse(self, response):
        ARTICLE_XPATH = "//div[contains(@class, 'tC')]//a"

        for a in response.xpath(ARTICLE_XPATH):
            title = a.xpath("./text()").get()
            href = a.xpath("./@href").get()

            print("parsing %s" %title)
            yield scrapy.Request(url=response.urljoin(href),
                callback=self.parse_article, meta={"title": title})

        page = str(int(response.meta["page"]) + 1)
        start_url = response.meta["start_url"]
        new_url = start_url + "page" + page + "/"
        request = scrapy.Request(url=new_url, callback=self.parse)
        request.meta["page"] = page
        request.meta["start_url"] = start_url
        yield request

    def parse_article(self, response):
        TEXT_XPATH = "//div[contains(@class, 'entry-content')]/p//text()"
        TIME_XPATH = "//div[contains(@class, 'header_byline')]/time/text()"

        title = response.meta["title"]
        url = response.url
        time = response.xpath(TIME_XPATH).get()
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
            with open('data/scraped_articles_topical.json', 'a') as outfile:
                json.dump(data, outfile)
        except Exception as e: print(e)