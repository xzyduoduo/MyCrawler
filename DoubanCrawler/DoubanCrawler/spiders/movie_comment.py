from scrapy import Request
from scrapy.spider import Spider
from ..items import MovieInfoItem, MovieCommentItem
from scrapy.shell import inspect_response


class DoubanMovieCommentSpider(Spider):
    name = 'DoubanMovieCommentSpider'
    start_urls = ['https://movie.douban.com/chart']
    headers = {
        'Accept': 'text/event-stream',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cookie': 'bid=HnCstpM_FOY; __yadk_uid=MMNHGsX1KRKJVBimbcelnJoO7S5EddVr; viewed="1406522_1085799"; ps=y; _ga=GA1.2.516320636.1481359486; _gid=GA1.2.1576398660.1505288920; dbcl2="147918655:r/RIYn//uJk"; ck=u98J; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1505293779%2C%22https%3A%2F%2Fmovie.douban.com%2Fchart%22%5D; loc-last-index-location-id="118159"; ll="118159"; __utma=30149280.516320636.1481359486.1505286885.1505293780.25; __utmb=30149280.28.10.1505293780; __utmc=30149280; __utmz=30149280.1505293780.25.13.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/chart; __utmv=30149280.14791; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=41281A232F4C696EBFEE4A9E24E24822|63dbe1b9ce1e453136fe19f1a4472301; ap=1; _pk_id.100001.8cb4=7b68d60142f012fa.1481359486.14.1505295251.1505289993.; _pk_ses.100001.8cb4=*',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
        # 'Host': 'push.douban.com:4397',
        # 'Origin': 'https://www.douban.com'
    }
    cookies = {'bid': 'HnCstpM_FOY'}
            #   'll': '108288',
            #   '__yadk_uid': 'MMNHGsX1KRKJVBimbcelnJoO7S5EddVr',
            #   '_vwo_uuid_v2': '41281A232F4C696EBFEE4A9E24E24822|63dbe1b9ce1e453136fe19f1a4472301'}

    def start_requests(self):
        yield Request(url=self.start_urls[0], headers=self.headers, callback=self.direct_comment, cookies=self.cookies)

    def direct_comment(self, response):
        names = response.xpath("//div[@class='pl2']/a/text()").extract()
        urls = response.xpath("//div[@class='pl2']/a/@href").extract()
        stars = response.xpath("//div[@class='pl2']/div/span[@class='rating_nums']/text()").extract()
        audiences = response.xpath("//div[@class='pl2']/div/span[3]/text()").re(r'(\d+)')
        for i in range(len(urls)):
            item = MovieInfoItem()
            item['movie_name'] = names[i*2].strip().strip('/').strip()
            item['movie_rate'] = stars[i]
            item['movie_comment_num'] = audiences[i]
            item['movie_id'] = urls[i].split('/')[-2]
            yield item
            comment_url = urls[i]+'comments'
            yield Request(comment_url, headers=self.headers, callback=self.parse,
                          meta={'movie_id': item['movie_id'], 'comment_url': comment_url}, cookies=self.cookies)

    def parse(self, response):
        movie_id, comment_url = response.meta['movie_id'], response.meta['comment_url']
        if movie_id:
            times = response.xpath('//span[@class="comment-time "]/@title').extract()
            authors = response.xpath('//span[@class="comment-info"]/a/text()').extract()
            votes = response.xpath('//span[@class="comment-vote"]/span/text()').extract()
            rates = response.xpath('//span[@class="comment-info"]/span[2]/@class').extract() # .re('(\\d+)')
            contents = response.xpath('//div[@class="comment"]/p/text()').extract()
            if times:
                for i in range(len(times)):
                    item = MovieCommentItem()
                    item['movie_id'] = movie_id
                    item['comment_time'] = times[i]
                    item['comment_author'] = authors[i]
                    item['comment_vote'] = votes[i]
                    item['comment_rate'] = rates[i]
                    item['comment_content'] = contents[i].strip('"').strip()
                    yield item
                next_url = comment_url + response.xpath('//div[@id="paginator"]/a/@href').extract()[-1]
                if next_url:
                    self.headers['referrer'] = comment_url
                    yield Request(next_url, headers=self.headers, callback=self.parse,
                                  meta={'movie_id': item['movie_id'], 'comment_url': comment_url}, cookies=self.cookies)
            else:
                inspect_response(response, self)
        else:
            inspect_response(response, self)
