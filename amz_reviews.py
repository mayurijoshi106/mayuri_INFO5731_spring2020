import scrapy
from scrapy.http import Request

# Creating a new class to implement Spide
class AmazonReviewsSpider(scrapy.Spider):
    
    custom_settings = {
      'CONCURRENT_REQUESTS':1,
      'DOWNLOAD_DELAY': 5
    }
    # Spider name
    name = 'amazon_reviews'
    allowed_domains = ["amazon.com"]    
    # Base URL for the MacBook air reviews
    myBaseUrl = "https://www.amazon.com/Dell-Inspiron-5000-5570-Laptop/product-reviews/B07N49F51N/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
    start_urls= []
    
    # Creating list of urls to be scraped by appending page number a the end of base url
    for i in range(1,9):
        start_urls.append(myBaseUrl+str(i))

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            yield Request(url=url, callback=self.parse_data, dont_filter=True)

    def parse_data(self, response):
      data = response.css('#cm_cr-review_list')
      names = data.css('.a-profile-name')
      stars = data.css('.review-rating')
      reviewTitles = data.css('.review-title')
      reviews = data.css('.review-text')
      count = 0

      # Combining the results
      for user in names:
          yield {'Name': ''.join(user.xpath('.//text()').extract()),
                 'Rating': ''.join(stars[count].xpath('.//text()').extract()),
                 'Titles': ''.join(reviewTitles[count].xpath('.//text()').extract()),
                 'Reviews': ''.join(reviews[count].xpath(".//text()").extract())
                 }
          count = count + 1