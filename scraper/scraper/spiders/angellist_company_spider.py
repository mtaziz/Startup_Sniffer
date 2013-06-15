from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

import json
from datetime import datetime
import os

class AngellistSpider(BaseSpider):
    name = "angellist_company"
    allowed_domains = ["angel.co"]

    token = "14026bd1a099ae7277d4b0766eab9528"

    start_urls = []
    for i in xrange(1, 100001, 50):
        cids = range(i, i+50)
        list_str = ",".join(map(str,cids))
        start_urls.append("https://api.angel.co/1/startups/batch?ids=%s&access_token=%s" % (list_str, token))

    def parse(self, response):
        content = response.body
        records = json.loads(content)
        if len(records) == 0:
            return
        
        for record in records:
            if record['hidden'] is True:
                continue
            
            fpath = "scraper/angellist_company_json/%s.json" % record['id']
            with open(fpath, "w") as fh:
                json.dump(record, fh)

