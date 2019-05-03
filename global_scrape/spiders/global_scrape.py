import scrapy
from global_scrape.items import GlobalItem
from datetime import datetime
import re
import idna


class Global(scrapy.Spider):
	name = "first_scraper"

	
	start_urls = ["https://www.globaltrade.net/United-States/expert-service-provider.html"]


	npages = 250

	 
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



		temp = re.sub(r'\n\b', ' ',str( response.xpath('//td/p/text()').extract()))
		temp1 = re.sub(r'\\n\b', ' ',temp)
		temp2 = re.sub(r'\\xa0\b', ' ',temp1)
		item['about'] = temp2
		match = ['http://www.' , 'https://www.' , 'www.' , '.com' , '\\nhttp:www.' , '\\xa0http:www.' , 'website:' , 'website']
		web = str(re.findall(r'[\w\.-]+http[\w\.-]+', temp2))
		
		
		if 'www.' not in web:
			matches = ['http://www.' , 'https://www.' , 'www.' , '.com']
			temp4= response.xpath('//td/a/text()').extract() 
			temp5= [si for si in temp4 if any(xsi in si for xsi in matches)]
			item['website'] = str(temp5).replace('\\n',' ')
		
		else :
			item['website'] = web

		
		matchers = ['English' , 'Spanish ' , 'Chinese' , 'Russian' , 'Hindi' , 'German']
		temp6 = response.xpath('//div[contains(@class,"section details")]/table/tr/td/text()').extract()
		temp7= [st for st in temp6 if any(xst in st for xst in matchers)]
		item['language_spoken'] = str(temp7).replace('\\n',' ')



		item['page_url'] = response.xpath("//meta[@property='og:url']/@content").extract()



		yield item
