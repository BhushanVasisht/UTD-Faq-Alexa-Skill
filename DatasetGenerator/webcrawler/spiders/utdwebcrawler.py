"""
Author:Arihant Chhajed
Description:Crawl Spider to extract urls of pages with faqs of UTD website
"""
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from webcrawler.items import UtdCrawlerItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from webcrawler.JsonProcessor.processor import DataSet
class UtdCrawler(CrawlSpider):
    # The name of the spider
    name = "utd_crawl"
    

    # The domains that are allowed (links to other domains are skipped)

    allowed_domains = []

    # The URLs to start with
    start_urls = []

    # This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_items, dont_filter=True)
    def __init__(self):

        with open('url_list.txt','r') as f:
            content = f.readlines()
        domains = [x.strip() for x in content]
        for line in domains:
            self.allowed_domains.append(line)
            self.start_urls.append('https://%s' % line)
        print("allowed_domains", self.allowed_domains)
    # Method for parsing items
    def parse_items(self, response):
        # The list of items that are found on the particular page
        # Only extract canonicalized and unique links (with respect to the current page)
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
            is_allowed = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = True
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = UtdCrawlerItem()
                item['url'] = link.url
                request = scrapy.Request(link.url, callback=self.parse_detail_page,errback=self.errback_httpbin,dont_filter=True)
                request.meta['item'] = item
               # Return all the found items
                yield request
    def parse_detail_page(self, response):
        question =  response.xpath('//h3/text()').getall()
        for i,x in enumerate(question):
            question[i]=x.strip()
        # question = response.css('strong::text').extract()
        answers= []
        for x in question:
            s = ""
            a = s.join(response.xpath("//h3[contains(., '%(x)s')]/following-sibling::node()/descendant-or-self::text()" % {'x': x}).extract())
            a = a.strip()
            answers.append(a)    
        print("question",question.__len__())
        print("Answers",answers.__len__())    
        item = response.meta['item']
        data = dict(zip(question, answers))
        d = DataSet(data)
        d.__storeDictionary__(item['url'])
      
        yield  item

    # for logging http errors while web crawling
    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))
        print("Failure",failure)
        #if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        #elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        #elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)