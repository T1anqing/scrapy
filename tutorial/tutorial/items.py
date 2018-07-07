# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CtripItem(scrapy.Item):
		in_place = scrapy.Field()
		inplace_pinyin = scrapy.Field()
		title = scrapy.Field()
		title_pinyin = scrapy.Field()
		title_url = scrapy.Field()
		score = scrapy.Field()
		place = scrapy.Field()
		image_urls = scrapy.Field()
		image_paths = scrapy.Field()
		images = scrapy.Field()
		comment_nums = scrapy.Field()
		nextpage = scrapy.Field()
		notice = scrapy.Field()