# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import codecs
import json
import MySQLdb
from scrapy.pipelines.images import ImagesPipeline
#from scrapy.exceptions import DropItem
#from scrapy.http import Request

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
		def __init__(self):
				self.file = codecs.open('tutorial.json','w',encoding='utf-8')
		def process_item(self, item, spider):
				lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
				self.file.write(lines)
				return item
		def spider_closed(self, spider):
				self.file.close()


class MysqlPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect('localhost', 'root', '', 'tourism', charset="utf8", use_unicode=True)
		self.cursor = self.conn.cursor()

	def process_item(self, item, spider):
		insert_sql = """
			insert into trip_ctrip(title, title_pinyin, title_url, score, in_place, inplace_pinyin, place, image_urls, notice, comment_nums) 
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
		"""
		self.cursor.execute(insert_sql, (item["title"], item["title_pinyin"], item["title_url"], item["score"], item["in_place"], item["inplace_pinyin"], item["place"], item["image_urls"], item["notice"], item["comment_nums"]))
		self.conn.commit()


class MyImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item