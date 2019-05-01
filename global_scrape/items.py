import scrapy


class GlobalItem(scrapy.Item):
    
	logo_url = scrapy.Field()
	title = scrapy.Field()
	sub_title = scrapy.Field()
	primary_location = scrapy.Field()
	area_of_expertise = scrapy.Field()
	about = scrapy.Field()
	website = scrapy.Field()
	language_spoken = scrapy.Field()
	page_url = scrapy.Field()
  
