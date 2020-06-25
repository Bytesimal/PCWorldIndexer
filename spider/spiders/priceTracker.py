#  Copyright © 2020 NeuroByte Tech. All rights reserved.
#
#  NeuroByte Tech is the Developer Company of Rohan Mathew.
#
#  Project: PriceTracker
#  File Name: priceTracker.py
#  Last Modified: 11/05/2020, 19:59

import scrapy as sr


class PriceTrackerSpider(sr.Spider):
    name = 'priceTracker'
    allowed_domains = ['currys.co.uk']
    start_urls = [
        'https://www.currys.co.uk/gbuk/computing-accessories/office-supplies/shredders/510_4422_32066_xx_ba00011093'
        '-bv00308995%7Cbv00308996%7Cbv00310231/xx-criteria.html']

    def parse(self, response):
        """First method called to parse each index page"""

        # Looping through each product on the page
        for product in response.css("div.productWrapper"):
            url = product.css("header.productTitle > a::attr(href)").extract_first().strip()

            yield sr.Request(url=url, callback=self.parse_product)

        # Following pagination links
        nxt_pg_url = [titleBtn.css("::attr(href)").extract_first()
                      for titleBtn in response.css("div > ul > li > a")
                      if len(titleBtn.css("::attr(title)").extract()) != 0][-1]

        if nxt_pg_url:
            yield sr.Request(url=nxt_pg_url, callback=self.parse)

    @staticmethod
    def parse_product(response):
        """Parses each product from the page and updates it on the databse"""

        product_id = response.css("p.prd-code::text").extract_first()[14:]
        full_name = response.css("img.product-image::attr(alt)").extract_first()
        brand = full_name.split()[0].strip()
        model = full_name[full_name.index(" ") + 1:]
        price = response.css("div.amounts > div > div > strong.current::text").extract()[-1][1:]
        price = float(price.replace(",", ""))
        available = len(response.css("li.nostock::text")) == 0

        yield {
            "id": product_id,
            "name": {
                "brand": brand,
                "model": model
            },
            "price": price,
            "available": available,
            "url": response.url
        }
