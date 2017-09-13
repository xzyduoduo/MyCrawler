from scrapy import Request
from scrapy.spiders import Spider
from ..items import MovieItem


class DoubanMovieSpider(Spider):
    name = 'DoubanMovieSpider'
    # allowed_domains = []
    # start_urls = ['https://movie.douban.com/top250']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    # 如果没有制定url， 此方法会被调用，必须返回一个可迭代对象
    # 如果此方法被重载， start_urls会被忽略
    def start_requests(self):
        url = 'https://movie.douban.com/top250'
        yield Request(url, headers=self.headers)

    # # 如果制定了url， 此方法会被调用来创建Request对象，仅仅初始化被调用一次
    # # 默认使用start_urls中的url生成Request对象，parse作为回调函数
    # def make_requests_from_url(url):
    #     pass

    def parse(self, response):
        item = MovieItem()
        movies = response.xpath('//ol[@class="grid_view"]/li')
        for movie in movies:
            item['ranking'] = movie.xpath(
                './/div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath(
                './/div[@class="hd"]/a/span[1]/text()').extract()[0]
            item['score'] = movie.xpath(
                './/div[@class="star"]/span[@class="rating_num"]/text()'
            ).extract()[0]
            item['score_num'] = movie.xpath(
                '//div[@class="star"]/span[4]/text()').re(r'(\d+)人评价')[0]
            yield item
        # next_url=response.xpath('//span[@class="next"]/a/@href').extract()
        # if next_url:
        #     next_url="https://movie.douban.com/top250" + next_url[0]
        #     yield Request(next_url, headers=self.headers)
