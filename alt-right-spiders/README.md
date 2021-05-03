# Alt-Right Spiders

## Instructions
1. Clone this repo
2. Install scrapy into your virtual environment e.g. `conda install scrapy` 
3. Run a spider from root using `scrapy runspider alt-right-spiders/alt-right-spiders/spiders breitbart.py`

Note: `amren.py`, `dailystormer.py` and `vdare.py` scrape the entire websites, whereas `brietbart.py` scraps the archive. They can be adjusted to scrape specific parts of the websites.

## Resources
[Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)