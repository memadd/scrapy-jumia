import scrapy
from bs4 import BeautifulSoup
import re
from jumia.items import JumiaItem


class Mobiles(scrapy.Spider):
    name = "mobile"

    start_urls = [
        'https://www.jumia.com.eg/phones-tablets/'
    ]

    def __init__(self):
        self.declare_xpath()

    def declare_xpath(self):
        self.getAllCategriesXpath = "/html/body/main/aside/section/section/ul/li/a/@href"
        self.getAllProductsXpath = "/html/body/main/section[2]/section[2]/div/a/@href"
        self.TitleXpath = "//*[@id='jm']/main/div[2]/section/div/div[2]/div[1]/div/h1/text()"
        self.CategoryXpath = "//*[@id='jm']/main/div[2]/div[1]/a[3]/text()"
        self.PriceCss = ".-fs24::text"
        self.DescriptionXpath = "//*[@id='jm']/main/div[3]/div[2]/section[1]/div[2]/article[1]/div/div/ul"
        self.ReviewsCss = ".-phm.-d-co div p::text"
        self.RateXpath = "//div[contains(@class,'-fs29 -yl5')]//text()"
        self.ImageLinkCss = "#imgs .-fh::attr(data-src)"
    def parse(self, response):
        for href in response.xpath(self.getAllCategriesXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url=url, callback=self.parse_caregory)

    def parse_caregory(self, response):
        for href in response.xpath(self.getAllProductsXpath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_main_item)

        next_page = response.xpath("/html/body/main/section[2]/section[3]/ul/li[6]/a/@href").extract_first()
        if next_page is not None:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, callback=self.parse_caregory, dont_filter=True)

    def parseText(self, x):
        soup = BeautifulSoup(x, 'html.parser')
        return re.sub(" +|\n|\r|\t|\0|\x0b|\xa0", ' ', soup.get_text()).strip()

    def parse_main_item(self, response):
        item = JumiaItem()

        Title = response.xpath(self.TitleXpath).get()

        Category = response.xpath(self.CategoryXpath).get()

        Price = response.css(self.PriceCss).get()
        #Price = self.parseText(Price)

        Description = response.xpath(self.TitleXpath).get()
        Description = self.parseText(Description)

        Reviews = response.css(self.ReviewsCss).extract()

        Rate = response.xpath(self.RateXpath).get()
        #Rate = self.parseText(Rate)
        Image_link = response.css(self.ImageLinkCss).extract()
        # Put each element into its item attribute.
        item['Title'] = Title
        item['Category'] = Category
        item['Price'] = Price
        item['Description'] = Description
        item['Reviews'] = Reviews
        item['Rate'] = Rate
        item['Image_link'] = Image_link
        return item
