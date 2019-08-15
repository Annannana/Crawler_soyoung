# -*- coding: utf-8 -*-
import scrapy
import json
from soyoung.items import SoyoungItem


class HospitalsSpider(scrapy.Spider):
    name = 'hospitals'
    allowed_domains = ['m.soyoung.com']

    def start_requests(self):
        for index in range(0, 2000):
            url = 'https://m.soyoung.com/hospitalsearch?ajax=1&index=' + str(index) + '&calendar_type=3&menu1_id=&select_id='
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hospitals = json.loads(response.text)['result']['view']['dphospital']
        if hospitals:
            for hospital in hospitals: # hospitals' specific information
                item = SoyoungItem()
                item['category'] = ['美容']
                item['name'] = hospital['name_cn']
                item['address'] = hospital['address']
                item['tag'] = [tag['menu1_name'] for tag in hospital['hot_menu1']]
                item['score'] = hospital['star']
                url = 'https://m.soyoung.com/y/hospital/'+ hospital['hospital_id'] + '/riji/?lver=0&_json=1'
                yield scrapy.Request(url=url, callback=self.parse_info, meta={'item': item})


    def parse_info(self, response):
        item = response.meta.get('item')
        json_text = json.loads(response.text)
        hospital_info = json_text['hospital_info']
        if hospital_info:
            hospital_cases = json_text['hospital_cases']
            phone = [hospital_info.get('hospital_tel'), hospital_info.get('service_tel')]
            item['phone'] = [p for p in phone if p]
            item['intro'] = hospital_info['intro']
            item['city'] = hospital_info['city']
            item['officalurl'] = hospital_info['website']
            item['qq'] =  hospital_info['service_qq']
            item['email'] = hospital_info['email']
            comments = []
            for case in hospital_cases:
                comment = dict()
                comment['comment_name'] = case['user_name']
                comment['comment_content'] = case['title']
                comment['comment_time'] = case['create_date']
                comments.append(comment)
            item['comment'] = comments
            yield item
