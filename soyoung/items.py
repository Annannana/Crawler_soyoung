import scrapy


class SoyoungItem(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    tag = scrapy.Field()
    score = scrapy.Field()
    phone = scrapy.Field()
    qq = scrapy.Field()
    email = scrapy.Field()
    category = scrapy.Field()
    comment = scrapy.Field()
    city = scrapy.Field()
    intro = scrapy.Field()
    officalurl = scrapy.Field()
    pass
