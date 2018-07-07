# -*- coding: utf-8 -*-
import scrapy
import csv
import re
from sys import argv
from scrapy.http import Request
from urllib import parse
from tutorial.items import CtripItem
from xpinyin import Pinyin

class CtripSpider(scrapy.Spider):
    name = "Ctrip"
    allowed_domains = ["you.ctrip.com"]
    start_urls = [
        #"http://you.ctrip.com/sight/beijing1/s0-p1.html"
        #"http://you.ctrip.com/sight/xian7/s0-p1.html"
        "http://you.ctrip.com/sight/chengdu104/s0-p1.html"
    ]

    def parse(self, response):
        for sel in response.xpath('//div[@class="list_mod2"]'):
            title_url = sel.xpath('div[@class="rdetailbox"]/dl/dt/a/@href').extract_first("")
            yield Request(url=parse.urljoin(response.url, title_url), callback=self.parse_detail)
        nextpage = response.xpath('//a[@class="nextpage"]/@href').extract_first()
        if nextpage:
            next = "http://you.ctrip.com/"+str(nextpage)
            yield scrapy.http.Request(next,callback = self.parse)
    
    def parse_detail(self, response):
        item = CtripItem()
        in_place = response.xpath('//div[@class="breadbar_v1 cf"]/ul/li[5]/a/text()').extract_first()
        title = response.xpath('//div[@class="f_left"]/h1/a/text()').extract_first()
        title_url = response.xpath('//div[@class="f_left"]/h1/a/@href').extract() 
        score = response.xpath('//span[@class="score"]/b/text()').extract()
        place = response.xpath('//div[@class="s_sight_infor"]/p/text()').extract() 
        notice = str(response.xpath('normalize-space(//div[@class="normalbox boxsight_v1"]/div[3]/div[2]/div/text())').extract())
        comment_nums = str(response.xpath('//div[@class="detailtab cf"]/ul/li/a/span/text()').extract())
        image_urls = response.xpath('//div[@class="carousel-inner"]/div[1]/a/img/@src').extract()
        #in_place = '北京'
        pin = Pinyin()
        #(re.sub('[^a-zA-Z]','','das .asd232'))
        title_pinyin = re.sub('[^a-zA-Z]','',pin.get_pinyin(title, ""))
        inplace_pinyin = re.sub('[^a-zA-Z]','',pin.get_pinyin(in_place, ""))

        item['in_place'] = in_place
        item['inplace_pinyin'] = inplace_pinyin
        item['title'] = title
        item['title_pinyin'] = title_pinyin
        item['title_url'] = title_url
        item['score'] = score
        item['place'] = place
        item['notice'] = notice
        item['comment_nums'] = comment_nums
        item['image_urls'] = image_urls
        yield item    

