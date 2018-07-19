# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem
import time
import traceback


class PositionSpider(scrapy.Spider):
    name = 'position'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=']

    def start_requests(self):
        """
        构建带cookie的request
        """
        return [
            scrapy.http.Request(
            url="http://www.lagou.com/jobs/list_python?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=",
            meta={"cookiejar": 1},
            callback=self.request_position,
          )]

    def request_position(self, response):
        """
        携带cookies请求ajax，得到json文件
        """
        #
        # position_sum = response.xpath('//a[@id="tab_pos"]/span/text()').extract()[0]
        # per_page = 15
        # if int(position_sum) % per_page == 0:
        #     page_sum = int(position_sum)/per_page
        # else:
        #     page_sum = int(position_sum)/per_page + 1
        # for pn in range(1, page_sum+1):
        #     #time.sleep(1)
        yield scrapy.http.FormRequest(
                url="https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false",
                formdata={"pn": '1', "kd": "python"},
                meta={"cookiejar": response.meta["cookiejar"]},
                callback=self.parse)

    def parse(self, response):
        """
        json.loads()将json格式转为python格式，按照html响应的json文件格式进行字典引用
        增加time.sleep()是防止出现KeyError: "content"错误， 应该是爬取页面太快， ajax未成功加载出
        """
        #time.sleep(10)
        jdict = json.loads(response.body)
        #time.sleep(10)
        try:
            jcontent = jdict["content"]["positionResult"]
        except Exception, e:
            print repr(e) + "?"*30
            jdict = json.loads(response.body)
            jcontent = jdict["content"]["positionResult"]
        finally:
            jresult = jcontent["result"]
            for each in jresult:
                item = LagouItem()
                item['city'] = each["city"].encode('utf-8')
                item['company'] = each["companyFullName"].encode('utf-8')
                item['size'] = each["companySize"].encode('utf-8')
                item['zone'] = each["district"].encode('utf-8')
                item['createtime'] = each["createTime"].encode('utf-8')
                item['labels'] = each["positionLables"].encode('utf-8')
                item['positionName'] = each["positionName"].encode('utf-8')
                item['salary'] = each["salary"].encode('utf-8')
                item['education'] = each["education"].encode('utf-8')
                item['workyear'] = each["workYear"].encode('utf-8')
                print "-" * 30
                yield item