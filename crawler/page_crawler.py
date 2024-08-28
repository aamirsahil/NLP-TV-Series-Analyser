import scrapy

class BlogSpider(scrapy.Spider):
    name = 'naruto_page'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        for href in response.css('.smw-columnlist-container')[0].css('a::attr(href)').extract():
            extracted_data = scrapy.Request('https://naruto.fandom.com/wiki/' + href,
                           callback=self._parse_page)
            yield extracted_data

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)

    def _parse_page(self, response):
        title = response.css("span.mw-page-title-main::text").extract()[0]
        title = title.strip()

        div_selector = response.css("div.mw-parser-output")[0]
        div_html = div_selector.extract()
        
        classification = 
        description = ""