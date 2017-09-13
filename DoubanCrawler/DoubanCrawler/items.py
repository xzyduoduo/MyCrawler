# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    ranking = scrapy.Field()
    movie_name = scrapy.Field()
    score = scrapy.Field()
    score_num = scrapy.Field()
    

class MovieInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_id = scrapy.Field()
    movie_name = scrapy.Field()
    movie_rate = scrapy.Field()
    movie_comment_num = scrapy.Field()


class MovieCommentItem(scrapy.Item):
    comment_time = scrapy.Field()
    comment_author = scrapy.Field()
    comment_vote = scrapy.Field()
    comment_rate = scrapy.Field()
    comment_content = scrapy.Field()
    movie_id = scrapy.Field()
