# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'

    def remove_characters(self, value):
        return value.strip('\xa0')

    def remove_quotes(self, value):
        return value.strip('"')

    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath(
            "//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:
            name = self.remove_quotes(product.xpath(
                "normalize-space(.//a[contains(@class, 'itemTitle')]/text())").get())
            storename1 = product.xpath(
                ".//a[contains(@class, 'itemStore')]/text()").get()
            storename2 = product.xpath(
                ".//button[contains(@class, 'itemStore')]/text()").get()
            if storename1:
                storename = self.remove_characters(storename1)
            else:
                storename = self.remove_characters(storename2)
            price = product.xpath(
                "normalize-space(.//div[contains(@class, 'itemPrice  wide')]/text())").get()

            # name = name.replace('"', '')
            #price = price.strip()
            yield {
                #    'brand':  product.xpath(".//a[@class='itemStore bp-p-storeLink bp-c-link']/text()").getall()
                'name': name,
                #  'name': product.xpath(".//a[@class='itemTile']/text()").get(),
                # 'link': product.xpath(".//a[@class='itemTile']/@href").get(),
                'storename': storename,
                'price': price
            }


'''
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=5,
                callback=self.parse
            )
'''
