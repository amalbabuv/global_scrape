import scrapy
from global_scrape.items import GlobalItem
from datetime import datetime
import re
import idna

class Global(scrapy.Spider):
	name = "first_scraper"

	
	start_urls = ["https://www.globaltrade.net/United-States/expert-service-provider.html"]

	npages = 3

	 
	for i in range(npages):
		start_urls.append("https://www.globaltrade.net/United-States/expert-service-provider.html?pageSize=10&orderBy=1&filterByPost=false&filterByRef=false&topicClear=false&industryClear=false&currentPage="+str(i)+"")
	


	def parse(self, response):
		for href in response.xpath("//p[contains(@class, 'sp-name')]/a[contains(@class, 'profileNavigator')]//@href"):
			
			url  = "https://www.globaltrade.net/" + href.extract() 
			yield scrapy.Request(url, callback=self.parse_dir_contents) 
	


	def parse_dir_contents(self, response):


		item = GlobalItem()


		item['logo_url'] = response.xpath('//div[contains(@class, "image")]/img[contains(@class,"lazy")]/@data-original').extract()[0]


		item['title']= response.xpath('//h1[contains(@class, "sp-title")]/span/text()').extract()[0]


		item['sub_title'] = response.xpath('//h4/span[contains(@class, "sub")]/text()').extract()[0]


		
		item['primary_location'] = response.xpath('//span[@itemprop = "addressLocality"]/text()').extract()[0].replace('\n',' ')

		
		item['area_of_expertise'] = response.xpath('//a[contains(@class, "mainExp")]/text()').extract()[0].replace('\n',' ')

		#temp3 = 
		item['about'] = response.xpath('//td/p/text()').extract()

		 
		item['website']  = response.xpath('//td/a/text()').extract()[1].replace('\n',' ')


		 
		item['language_spoken'] = response.xpath('//div[contains(@class,"section details")]/table/tr/td/text()').extract()[15].replace('\n',' ')


		item['page_url'] = response.xpath("//meta[@property='og:url']/@content").extract()


		yield item
