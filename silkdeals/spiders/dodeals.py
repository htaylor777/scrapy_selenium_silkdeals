# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.keys import Keys


class DodealsSpider(scrapy.Spider):
    name = 'dodeals'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://duckgo.com",
            wait_time=3,
            screenshot=True,
            callback=self.parse)

    def parse(self, response):
        #    img = response.request.meta['screenshot']

        #   with open('screenshot.png', 'wb') as f:
        #        f.write(img)
        driver = response.meta['driver']
        search_input = driver.find_element_by_xpath(
            "//input[@id='search_form_input_homepage']")
        search_input.send_keys('Apple')
        search_input.send_keys(Keys.ENTER)

        html = driver.page_source
        response_obj = Selector(text=html)
        driver.save_screenshot('EnteredAppt.png')

        links = response_obj.xpath("//div[@class='result_extras_url']/a")
        for link in links:
            yield{
                'URL': link.xpath(".//@href").get()
            }
