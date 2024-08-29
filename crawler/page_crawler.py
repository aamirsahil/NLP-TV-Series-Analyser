import scrapy
from bs4 import BeautifulSoup

class BlogSpider(scrapy.Spider):
    name = 'naruto_page'
    start_urls = ['https://naruto.fandom.com/wiki/Special:BrowseData/Jutsu?limit=250&offset=0&_cat=Jutsu']

    def parse(self, response):
        for href in response.css('.smw-columnlist-container')[0].css('a::attr(href)').extract():
            extracted_data = scrapy.Request('https://naruto.fandom.com' + href,
                           callback=self._parse_page)
            yield extracted_data

        for next_page in response.css('a.mw-nextlink'):
            yield response.follow(next_page, self.parse)

    def _parse_page(self, response):
        
        title = ""
        classification = ""
        description = ""

        title = response.css("span.mw-page-title-main::text").extract()[0]
        title = title.strip()

        div_selector = response.css("div.mw-parser-output")[0]
        div_html = div_selector.extract()

        soup = BeautifulSoup(div_html).find('div')

        if soup.find('aside'):
            aside = soup.find('aside')

            for cell in aside.find_all('div', {'class' : 'pi-data'}):
                if cell.find('h3'):
                    cell_name = cell.find('h3').text.strip()
                    if cell_name == "Classification":
                        classification = cell.find('div').text.strip()
            
            soup.find('aside').decompose()
            description = soup.text.strip()
            description = description.split('Trivia')[0].strip()
        
        return dict(
            jutsu_name = title,
            justsu_type = classification,
            jutsu_description = description)