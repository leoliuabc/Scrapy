import scrapy
from ..items import ImgspiderItem
import re

class ImgSpider(scrapy.Spider):
    name = 'ImgSpider'
    allowed_domains = ['www.joliplacard.com']
    base_url = 'https://www.joliplacard.com'
    start_urls = ['https://www.joliplacard.com/collections/all']
    productList_xpath = "//div[@class='item product-index desktop-3 tablet-2 mobile-half']"
    url_xpath = "./div[@class='product-info']/a/@href"
    product_name_xpath = "./div[@class='product-info']/a/@href"
    nextPage_xpath = "//link[@rel='next']/@href"
    image_urls_xpath = "//img[@class='product__image lazyload lazyload-fade']/@src"
    count = 1
    page_end = 18

    def parse(self, response):
        productList = response.xpath(self.productList_xpath)
        for product in productList:
            item = ImgspiderItem()
            item['url'] = self.base_url + product.xpath(self.url_xpath).extract_first()
            item['product_name'] = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", product.xpath(self.product_name_xpath).extract_first())
            yield scrapy.Request(item['url'], meta={'item': item}, callback=self.img_parse)

        nextPage = response.xpath(self.nextPage_xpath).extract_first()
        if self.count < self.page_end:
            if nextPage is not None:
                self.count = self.count + 1
                yield scrapy.Request(self.base_url + nextPage, callback=self.parse)
        else:
            return None

        # if self.count < self.page_end:
        #     self.count = self.count + 1
        #     next_page = self.start_urls[0] + '?page_size=' + str(self.count)
        #     yield scrapy.Request(self.base_url + next_page, callback=self.parse)
        # else:
        #     return None

    def img_parse(self, response):
        item = response.meta['item']
        image_urls = response.xpath(self.image_urls_xpath).extract()
        item['img_name'] = []
        item['image_urls'] = ['http:' + x for x in image_urls]
        for num in range(1, len(image_urls)):
            item['img_name'].append(str(num))
        yield item
