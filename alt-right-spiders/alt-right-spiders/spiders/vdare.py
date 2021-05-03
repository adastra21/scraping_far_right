import scrapy
from datetime import datetime
import json

class VDARESpider(scrapy.Spider):
    name = "vdare_spider"

    def start_requests(self):        
        start_urls = [
        "https://vdare.com/articles",
        "https://vdare.com/posts",
        "https://vdare.com/letters"
        ]
        for url in start_urls:
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta["page"] = 1
            request.meta["start_url"] = url
            yield request
    
    def parse(self, response):
        ARTICLE_XPATH = "//a[contains(@class, 'mb-1')]"

        for a in response.xpath(ARTICLE_XPATH):
            title = a.xpath("./h2/text()").get()
            href = a.xpath("./@href").get()

            print("parsing %s" %title)
            yield scrapy.Request(url=response.urljoin(href),
                callback=self.parse_article, meta={"title": title})

        page = str(int(response.meta["page"]) + 1)
        start_url = response.meta["start_url"]
        next_url = start_url + "?page=" + page
        print("scraping %s" %next_url)
        request = scrapy.Request(url=next_url, callback=self.parse)
        request.meta["page"] = page
        request.meta["start_url"] = start_url
        yield request

    def parse_article(self, response):
        TEXT_XPATH = "//div[contains(@class, 'publication-content__content-block')]//text()"
        TIME_XPATH = "//div[contains(@class, 'pub-date')]//text()"

        title = response.meta["title"]
        url = response.url
        time = response.xpath(TIME_XPATH).get()
        text = response.xpath(TEXT_XPATH).getall()

        # fix time formatting
        time = datetime.strptime(time, "%m/%d/%Y")
        time = time.isoformat()

        data = {"title": title,
                "text": text,
                "link": url,
                "published": time}
        
        try:
            # update filename
            with open('data/scraped_articles_vdar.json', 'a') as outfile:
                json.dump(data, outfile)
        except Exception as e: print(e)