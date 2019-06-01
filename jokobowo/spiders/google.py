import scrapy
import re


def is_google(a):
    url = a.attrib['href']
    return bool(re.search("/search", url))


def test():
    print('test')

class QuotesSpider(scrapy.Spider):
    name = "google"

    start_urls = [
        'https://www.google.com/search?q=prabowo&safe=strict&ei=sLTvXL_KH4zfz7sPpZOBuA4&start=%s&sa=N&ved=0ahUKEwi_4un2icPiAhWM73MBHaVJAOc4ChDx0wMIjQE&cshid=1559213273144254&biw=1680&bih=916' % start for start in range(0, 100, 10)
    ]

    def parse(self, response):
        for href in response.css('.jfp3ef a'):
            if not is_google(href):
                yield response.follow(href, self.parse_text)

    def parse_text(self, response):
        def get_text(response):
            with_duplicated_space = ' '.join(response.xpath(
                './/text()[not(ancestor::script|ancestor::style|ancestor::noscript)]').extract()).strip().replace("\r", "").replace("\n", "").replace("\t", "")
            without_duplicated_space = re.sub(
                ' +', ' ', with_duplicated_space).strip()
            return without_duplicated_space
        yield {
            'title': response.css('title::text').get(),
            'text': get_text(response)
        }


# %%
